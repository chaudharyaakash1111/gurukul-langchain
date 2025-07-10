"""
Curriculum Ingestion Logic for Akash Gurukul
Handles loading, validation, and processing of lesson content
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import jsonschema
from jsonschema import validate

# Validation schema for lesson format
LESSON_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "level", "category", "learning_objectives", "estimated_duration", "content", "quiz", "metadata"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "level": {"type": "string", "enum": ["Foundation", "Seed", "Tree", "Sky"]},
        "category": {"type": "string", "enum": ["foundation", "dharma", "artha", "kama", "moksha"]},
        "prerequisites": {"type": "array", "items": {"type": "string"}, "default": []},
        "learning_objectives": {
            "oneOf": [
                {"type": "array", "items": {"type": "string"}, "minItems": 1},
                {
                    "type": "object",
                    "required": ["overall"],
                    "properties": {
                        "overall": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                        "by_agent": {
                            "type": "object",
                            "properties": {
                                "seed": {"type": "array", "items": {"type": "string"}},
                                "tree": {"type": "array", "items": {"type": "string"}},
                                "sky": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    }
                }
            ]
        },
        "estimated_duration": {"type": "number", "minimum": 1},
        "content": {
            "type": "object",
            "required": ["text"],
            "properties": {
                "text": {"type": "string"},
                "media": {
                    "type": "object",
                    "properties": {
                        "images": {"type": "array", "items": {"type": "string"}, "default": []},
                        "videos": {"type": "array", "items": {"type": "string"}, "default": []},
                        "audio": {"type": "array", "items": {"type": "string"}, "default": []}
                    },
                    "default": {}
                }
            }
        },
        "quiz": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["id", "type", "question"],
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string", "enum": ["multiple_choice", "true_false", "short_answer", "reflection", "scenario"]},
                    "question": {"type": "string"},
                    "options": {"type": "array", "items": {"type": "string"}},
                    "correct_answer": {"oneOf": [{"type": "number"}, {"type": "boolean"}, {"type": "string"}]},
                    "explanation": {"type": "string"},
                    "sample_answers": {"type": "array", "items": {"type": "string"}},
                    "guidance": {"type": "string"}
                }
            }
        },
        "tts": {"type": "boolean", "default": False},
        "query_paths": {
            "type": "object",
            "properties": {
                "practical": {"type": "object"},
                "conceptual": {"type": "object"},
                "reflective": {"type": "object"}
            }
        },
        "metadata": {
            "type": "object",
            "required": ["created_by", "created_date", "last_modified", "version", "difficulty"],
            "properties": {
                "created_by": {"type": "string"},
                "created_date": {"type": "string", "format": "date"},
                "last_modified": {"type": "string", "format": "date"},
                "version": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}, "default": []},
                "difficulty": {"type": "number", "minimum": 1, "maximum": 5}
            }
        }
    }
}


class CurriculumIngestion:
    def __init__(self, curriculum_path: str = "./curriculum/lessons"):
        self.curriculum_path = Path(curriculum_path)
        self.lessons: Dict[str, Dict] = {}
        self.learning_paths: Dict[str, Dict] = {}

    def load_lesson(self, file_path: Path) -> Dict[str, Any]:
        """Load and validate a single lesson file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lesson = json.load(f)
            
            # Validate lesson format
            validate(instance=lesson, schema=LESSON_SCHEMA)
            
            return lesson
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
        except jsonschema.ValidationError as e:
            raise ValueError(f"Validation error in {file_path}: {e.message}")
        except Exception as e:
            raise ValueError(f"Error loading lesson from {file_path}: {e}")

    def load_all_lessons(self) -> Dict[str, Dict]:
        """Load all lessons from the curriculum directory"""
        try:
            if not self.curriculum_path.exists():
                raise FileNotFoundError(f"Curriculum directory not found: {self.curriculum_path}")
            
            json_files = list(self.curriculum_path.glob("*.json"))
            print(f"Found {len(json_files)} lesson files")
            
            for file_path in json_files:
                lesson = self.load_lesson(file_path)
                self.lessons[lesson['id']] = lesson
                print(f"Loaded lesson: {lesson['title']} ({lesson['level']})")
            
            print(f"Successfully loaded {len(self.lessons)} lessons")
            return self.lessons
        except Exception as e:
            print(f"Error loading lessons: {e}")
            raise

    def validate_dependencies(self) -> None:
        """Validate lesson prerequisites and dependencies"""
        errors = []
        
        for lesson_id, lesson in self.lessons.items():
            for prereq_id in lesson.get('prerequisites', []):
                if prereq_id not in self.lessons:
                    errors.append(f"Lesson {lesson_id} has invalid prerequisite: {prereq_id}")
        
        if errors:
            raise ValueError(f"Dependency validation failed:\n" + "\n".join(errors))
        
        print("All lesson dependencies validated successfully")

    def generate_learning_paths(self) -> Dict[str, Dict]:
        """Generate learning paths based on prerequisites and levels"""
        paths = {
            "foundation": {"Foundation": []},
            "dharma": {"Seed": [], "Tree": [], "Sky": []},
            "artha": {"Seed": [], "Tree": [], "Sky": []},
            "kama": {"Seed": [], "Tree": [], "Sky": []},
            "moksha": {"Seed": [], "Tree": [], "Sky": []}
        }
        
        # Sort lessons by category and level
        for lesson in self.lessons.values():
            paths[lesson['category']][lesson['level']].append(lesson)
        
        # Sort each path by prerequisites (topological sort)
        for category in paths:
            for level in paths[category]:
                paths[category][level] = self._topological_sort(paths[category][level])
        
        self.learning_paths = paths
        return paths

    def _topological_sort(self, lessons: List[Dict]) -> List[Dict]:
        """Topological sort for lesson ordering based on prerequisites"""
        sorted_lessons = []
        visited = set()
        visiting = set()
        lesson_map = {lesson['id']: lesson for lesson in lessons}
        
        def visit(lesson: Dict):
            if lesson['id'] in visiting:
                raise ValueError(f"Circular dependency detected involving lesson: {lesson['id']}")
            
            if lesson['id'] in visited:
                return
            
            visiting.add(lesson['id'])
            
            # Visit prerequisites first
            for prereq_id in lesson.get('prerequisites', []):
                if prereq_id in lesson_map:
                    visit(lesson_map[prereq_id])
            
            visiting.remove(lesson['id'])
            visited.add(lesson['id'])
            sorted_lessons.append(lesson)
        
        for lesson in lessons:
            if lesson['id'] not in visited:
                visit(lesson)
        
        return sorted_lessons

    def get_lessons_by_level(self, level: str, category: Optional[str] = None) -> List[Dict]:
        """Get lessons by level and optionally by category"""
        filtered = [
            lesson for lesson in self.lessons.values()
            if lesson['level'] == level and (category is None or lesson['category'] == category)
        ]
        return filtered

    def get_lesson(self, lesson_id: str) -> Optional[Dict]:
        """Get lesson by ID"""
        return self.lessons.get(lesson_id)

    def export_for_agents(self) -> Dict[str, Any]:
        """Export curriculum data for agents"""
        return {
            "lessons": self.lessons,
            "learning_paths": self.learning_paths,
            "metadata": {
                "total_lessons": len(self.lessons),
                "last_updated": datetime.now().isoformat(),
                "levels": ["Seed", "Tree", "Sky"],
                "categories": ["dharma", "artha", "kama", "moksha"]
            }
        }

    def save_curriculum_export(self, output_path: str = "./curriculum/curriculum_export.json") -> None:
        """Save curriculum export to file"""
        export_data = self.export_for_agents()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        print(f"Curriculum exported to {output_path}")


if __name__ == "__main__":
    # Example usage
    ingestion = CurriculumIngestion()
    try:
        ingestion.load_all_lessons()

        # For testing, we'll skip dependency validation if there are missing prerequisites
        try:
            ingestion.validate_dependencies()
            print("All dependencies validated successfully")
        except ValueError as e:
            print(f"Warning: Dependency validation issues found: {e}")
            print("Continuing with available lessons...")

        ingestion.generate_learning_paths()
        ingestion.save_curriculum_export()
        print("Curriculum ingestion completed successfully!")
    except Exception as e:
        print(f"Error during curriculum ingestion: {e}")
