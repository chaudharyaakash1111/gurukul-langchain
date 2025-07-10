"""
Audio/Video Sync Framework for Akash Gurukul
Handles timestamped audio chunks and video asset integration with graceful fallbacks
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime

@dataclass
class AudioChunk:
    """Represents a timestamped audio segment"""
    id: str
    start_time: float  # seconds
    end_time: float    # seconds
    text: str          # corresponding text
    file_path: str     # path to audio file
    speaker: Optional[str] = None  # agent type or narrator

@dataclass
class VideoAsset:
    """Represents a video asset with timing information"""
    id: str
    file_path: str
    start_time: float
    duration: float
    asset_type: str    # "illustration", "animation", "background"
    description: str

@dataclass
class SyncPoint:
    """Synchronization point between audio, video, and text"""
    timestamp: float
    text_position: int  # character position in text
    audio_chunk_id: Optional[str] = None
    video_asset_id: Optional[str] = None
    subtitle_text: Optional[str] = None

class MediaSyncManager:
    """Manages synchronization between audio, video, and text content"""
    
    def __init__(self, lesson_id: str, media_base_path: str = "./media"):
        self.lesson_id = lesson_id
        self.media_base_path = Path(media_base_path)
        self.media_base_path.mkdir(exist_ok=True)
        
        # Storage for media assets
        self.audio_chunks: List[AudioChunk] = []
        self.video_assets: List[VideoAsset] = []
        self.sync_points: List[SyncPoint] = []
        
        # Load existing sync data if available
        self._load_sync_data()
    
    def _load_sync_data(self):
        """Load existing synchronization data"""
        sync_file = self.media_base_path / f"{self.lesson_id}_sync.json"
        if sync_file.exists():
            try:
                with open(sync_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load audio chunks
                for chunk_data in data.get('audio_chunks', []):
                    self.audio_chunks.append(AudioChunk(**chunk_data))
                
                # Load video assets
                for asset_data in data.get('video_assets', []):
                    self.video_assets.append(VideoAsset(**asset_data))
                
                # Load sync points
                for sync_data in data.get('sync_points', []):
                    self.sync_points.append(SyncPoint(**sync_data))
                    
            except Exception as e:
                print(f"Error loading sync data: {e}")
    
    def _save_sync_data(self):
        """Save synchronization data"""
        sync_file = self.media_base_path / f"{self.lesson_id}_sync.json"
        
        data = {
            "lesson_id": self.lesson_id,
            "last_updated": datetime.now().isoformat(),
            "audio_chunks": [
                {
                    "id": chunk.id,
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "text": chunk.text,
                    "file_path": chunk.file_path,
                    "speaker": chunk.speaker
                }
                for chunk in self.audio_chunks
            ],
            "video_assets": [
                {
                    "id": asset.id,
                    "file_path": asset.file_path,
                    "start_time": asset.start_time,
                    "duration": asset.duration,
                    "asset_type": asset.asset_type,
                    "description": asset.description
                }
                for asset in self.video_assets
            ],
            "sync_points": [
                {
                    "timestamp": point.timestamp,
                    "text_position": point.text_position,
                    "audio_chunk_id": point.audio_chunk_id,
                    "video_asset_id": point.video_asset_id,
                    "subtitle_text": point.subtitle_text
                }
                for point in self.sync_points
            ]
        }
        
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_audio_chunk(self, chunk_id: str, start_time: float, end_time: float, 
                       text: str, file_path: str, speaker: str = None) -> AudioChunk:
        """Add a timestamped audio chunk"""
        chunk = AudioChunk(
            id=chunk_id,
            start_time=start_time,
            end_time=end_time,
            text=text,
            file_path=file_path,
            speaker=speaker
        )
        
        self.audio_chunks.append(chunk)
        self._save_sync_data()
        return chunk
    
    def add_video_asset(self, asset_id: str, file_path: str, start_time: float,
                       duration: float, asset_type: str, description: str) -> VideoAsset:
        """Add a video asset with timing"""
        asset = VideoAsset(
            id=asset_id,
            file_path=file_path,
            start_time=start_time,
            duration=duration,
            asset_type=asset_type,
            description=description
        )
        
        self.video_assets.append(asset)
        self._save_sync_data()
        return asset
    
    def create_sync_point(self, timestamp: float, text_position: int,
                         audio_chunk_id: str = None, video_asset_id: str = None,
                         subtitle_text: str = None) -> SyncPoint:
        """Create a synchronization point"""
        sync_point = SyncPoint(
            timestamp=timestamp,
            text_position=text_position,
            audio_chunk_id=audio_chunk_id,
            video_asset_id=video_asset_id,
            subtitle_text=subtitle_text
        )
        
        self.sync_points.append(sync_point)
        self.sync_points.sort(key=lambda x: x.timestamp)  # Keep sorted by time
        self._save_sync_data()
        return sync_point
    
    def get_media_at_time(self, timestamp: float, buffer_time: float = 0.1) -> Dict[str, Any]:
        """Get all media assets that should be active at a given timestamp with enhanced buffering"""
        result = {
            "audio_chunk": None,
            "video_assets": [],
            "subtitle_text": None,
            "sync_point": None,
            "upcoming_events": [],
            "buffer_status": "ready"
        }

        # Find active audio chunk with buffering
        for chunk in self.audio_chunks:
            if chunk.start_time <= timestamp <= chunk.end_time:
                result["audio_chunk"] = chunk
                break

        # Find active video assets with overlap handling
        for asset in self.video_assets:
            asset_end = asset.start_time + asset.duration
            if asset.start_time <= timestamp <= asset_end:
                result["video_assets"].append(asset)

        # Find nearest sync point with improved tolerance
        sync_tolerance = 0.3  # Increased tolerance for better sync
        best_sync_point = None
        min_distance = float('inf')

        for sync_point in self.sync_points:
            distance = abs(sync_point.timestamp - timestamp)
            if distance <= sync_tolerance and distance < min_distance:
                best_sync_point = sync_point
                min_distance = distance

        if best_sync_point:
            result["sync_point"] = best_sync_point
            result["subtitle_text"] = best_sync_point.subtitle_text

        # Find upcoming events for preloading
        upcoming_window = 2.0  # Look ahead 2 seconds
        for chunk in self.audio_chunks:
            if timestamp < chunk.start_time <= timestamp + upcoming_window:
                result["upcoming_events"].append({
                    "type": "audio",
                    "start_time": chunk.start_time,
                    "asset": chunk
                })

        for asset in self.video_assets:
            if timestamp < asset.start_time <= timestamp + upcoming_window:
                result["upcoming_events"].append({
                    "type": "video",
                    "start_time": asset.start_time,
                    "asset": asset
                })

        # Determine buffer status
        if len(result["upcoming_events"]) > 0:
            next_event_time = min(event["start_time"] for event in result["upcoming_events"])
            if next_event_time - timestamp < buffer_time:
                result["buffer_status"] = "buffering"

        return result
    
    def generate_playback_timeline(self) -> List[Dict[str, Any]]:
        """Generate a complete timeline for media playback"""
        timeline = []
        
        # Combine all timestamps
        all_timestamps = set()
        
        for chunk in self.audio_chunks:
            all_timestamps.add(chunk.start_time)
            all_timestamps.add(chunk.end_time)
        
        for asset in self.video_assets:
            all_timestamps.add(asset.start_time)
            all_timestamps.add(asset.start_time + asset.duration)
        
        for sync_point in self.sync_points:
            all_timestamps.add(sync_point.timestamp)
        
        # Create timeline entries
        for timestamp in sorted(all_timestamps):
            media_state = self.get_media_at_time(timestamp)
            timeline.append({
                "timestamp": timestamp,
                "media_state": media_state
            })
        
        return timeline
    
    def get_fallback_content(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback content when audio/video isn't available"""
        return {
            "mode": "text_only",
            "content": {
                "text": lesson_data.get("content", {}).get("text", ""),
                "images": lesson_data.get("content", {}).get("media", {}).get("images", []),
                "fallback_message": "Audio and video content is being prepared. You can still learn from the text content below.",
                "estimated_media_ready": "Audio and visual elements will be available soon to enhance your learning experience."
            },
            "interactive_elements": {
                "text_to_speech_available": False,
                "video_illustrations_available": False,
                "audio_narration_available": False
            }
        }
    
    def check_media_availability(self) -> Dict[str, bool]:
        """Check which media types are available for this lesson"""
        audio_available = len(self.audio_chunks) > 0 and all(
            Path(chunk.file_path).exists() for chunk in self.audio_chunks
        )
        
        video_available = len(self.video_assets) > 0 and all(
            Path(asset.file_path).exists() for asset in self.video_assets
        )
        
        sync_available = len(self.sync_points) > 0
        
        return {
            "audio_available": audio_available,
            "video_available": video_available,
            "sync_available": sync_available,
            "full_multimedia": audio_available and video_available and sync_available
        }
    
    def get_lesson_media_config(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get complete media configuration for a lesson"""
        availability = self.check_media_availability()
        
        if availability["full_multimedia"]:
            return {
                "mode": "full_multimedia",
                "timeline": self.generate_playback_timeline(),
                "audio_chunks": [
                    {
                        "id": chunk.id,
                        "start_time": chunk.start_time,
                        "end_time": chunk.end_time,
                        "file_path": chunk.file_path,
                        "speaker": chunk.speaker
                    }
                    for chunk in self.audio_chunks
                ],
                "video_assets": [
                    {
                        "id": asset.id,
                        "file_path": asset.file_path,
                        "start_time": asset.start_time,
                        "duration": asset.duration,
                        "asset_type": asset.asset_type
                    }
                    for asset in self.video_assets
                ]
            }
        elif availability["audio_available"]:
            return {
                "mode": "audio_with_text",
                "audio_chunks": [
                    {
                        "id": chunk.id,
                        "start_time": chunk.start_time,
                        "end_time": chunk.end_time,
                        "file_path": chunk.file_path,
                        "text": chunk.text
                    }
                    for chunk in self.audio_chunks
                ],
                "fallback_content": self.get_fallback_content(lesson_data)
            }
        else:
            return self.get_fallback_content(lesson_data)

    def create_buffered_timeline(self, buffer_seconds: float = 1.0) -> List[Dict[str, Any]]:
        """Generate timeline with buffering events for smooth playback"""
        timeline = []
        all_events = []

        # Collect all media events
        for chunk in self.audio_chunks:
            all_events.append({
                "timestamp": chunk.start_time - buffer_seconds,
                "type": "buffer_audio",
                "asset": chunk
            })
            all_events.append({
                "timestamp": chunk.start_time,
                "type": "play_audio",
                "asset": chunk
            })
            all_events.append({
                "timestamp": chunk.end_time,
                "type": "stop_audio",
                "asset": chunk
            })

        for asset in self.video_assets:
            all_events.append({
                "timestamp": asset.start_time - buffer_seconds,
                "type": "buffer_video",
                "asset": asset
            })
            all_events.append({
                "timestamp": asset.start_time,
                "type": "play_video",
                "asset": asset
            })
            all_events.append({
                "timestamp": asset.start_time + asset.duration,
                "type": "stop_video",
                "asset": asset
            })

        for sync_point in self.sync_points:
            all_events.append({
                "timestamp": sync_point.timestamp,
                "type": "sync_point",
                "asset": sync_point
            })

        # Sort events by timestamp
        all_events.sort(key=lambda x: x["timestamp"])

        # Group events by timestamp for simultaneous execution
        current_time = None
        current_group = []

        for event in all_events:
            if event["timestamp"] < 0:  # Skip negative timestamps
                continue

            if current_time is None or abs(event["timestamp"] - current_time) < 0.01:
                current_group.append(event)
                current_time = event["timestamp"]
            else:
                if current_group:
                    timeline.append({
                        "timestamp": current_time,
                        "events": current_group.copy()
                    })
                current_group = [event]
                current_time = event["timestamp"]

        # Add final group
        if current_group:
            timeline.append({
                "timestamp": current_time,
                "events": current_group
            })

        return timeline

    def get_sync_quality_metrics(self) -> Dict[str, Any]:
        """Analyze sync quality and provide metrics"""
        metrics = {
            "total_audio_chunks": len(self.audio_chunks),
            "total_video_assets": len(self.video_assets),
            "total_sync_points": len(self.sync_points),
            "coverage_analysis": {},
            "gap_analysis": [],
            "overlap_analysis": []
        }

        if not self.audio_chunks and not self.video_assets:
            return metrics

        # Calculate total timeline duration
        max_time = 0
        if self.audio_chunks:
            max_time = max(max_time, max(chunk.end_time for chunk in self.audio_chunks))
        if self.video_assets:
            max_time = max(max_time, max(asset.start_time + asset.duration for asset in self.video_assets))

        # Analyze coverage
        audio_coverage = 0
        for chunk in self.audio_chunks:
            audio_coverage += chunk.end_time - chunk.start_time

        video_coverage = 0
        for asset in self.video_assets:
            video_coverage += asset.duration

        metrics["coverage_analysis"] = {
            "timeline_duration": max_time,
            "audio_coverage": audio_coverage,
            "video_coverage": video_coverage,
            "audio_coverage_percentage": (audio_coverage / max_time * 100) if max_time > 0 else 0,
            "video_coverage_percentage": (video_coverage / max_time * 100) if max_time > 0 else 0
        }

        # Analyze gaps in audio
        sorted_audio = sorted(self.audio_chunks, key=lambda x: x.start_time)
        for i in range(len(sorted_audio) - 1):
            current_end = sorted_audio[i].end_time
            next_start = sorted_audio[i + 1].start_time
            if next_start > current_end:
                metrics["gap_analysis"].append({
                    "type": "audio_gap",
                    "start": current_end,
                    "end": next_start,
                    "duration": next_start - current_end
                })

        # Analyze overlaps
        for i, chunk1 in enumerate(self.audio_chunks):
            for chunk2 in self.audio_chunks[i + 1:]:
                if (chunk1.start_time < chunk2.end_time and
                    chunk2.start_time < chunk1.end_time):
                    metrics["overlap_analysis"].append({
                        "type": "audio_overlap",
                        "chunk1_id": chunk1.id,
                        "chunk2_id": chunk2.id,
                        "overlap_start": max(chunk1.start_time, chunk2.start_time),
                        "overlap_end": min(chunk1.end_time, chunk2.end_time)
                    })

        return metrics
