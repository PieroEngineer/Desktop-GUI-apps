import sounddevice as sd
import numpy as np
import threading
import time


class RecordModel:
    """
    MVC Model: Handles audio recording and processing logic.
    """
    def __init__(self):
        self.samplerate = 44100
        self.channels = 1
        self._audio_frames = []
        self._stream = None
        self._recording_thread = None
        self._is_recording = False
        self._max_seconds = None

    def _callback(self, indata, frames, time_info, status):
        """Internal callback used by sounddevice.InputStream"""
        if status:
            print(f"⚠️ Stream status: {status}")
        self._audio_frames.append(indata.copy())

    def _record_loop(self):
        """Internal method to record audio in a background thread."""
        self._audio_frames.clear()
        self._is_recording = True
        start_time = time.time()

        print("🎙️ Recording started...")

        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=self._callback):
            while self._is_recording:
                if self._max_seconds and (time.time() - start_time) >= self._max_seconds:
                    print("⏱️ Max recording time reached.")
                    self._is_recording = False
                    break
                time.sleep(0.1)

        print("🛑 Recording stopped.")

    def start_recording(self, max_seconds=None):
        """
        Starts recording in a background thread.
        If max_seconds is provided, stops automatically after that time.
        """
        if self._is_recording:
            print("⚠️ Already recording.")
            return

        self._max_seconds = max_seconds
        self._recording_thread = threading.Thread(target=self._record_loop, daemon=True)
        self._recording_thread.start()

    def stop_recording(self):
        """Stops the current recording."""
        if not self._is_recording:
            print("⚠️ No active recording to stop.")
            return

        self._is_recording = False
        if self._recording_thread is not None:
            self._recording_thread.join()

    def get_audio_data(self):
        """
        Returns the recorded audio as a NumPy array.
        """
        if not self._audio_frames:
            print("⚠️ No audio recorded.")
            return np.zeros((0, self.channels))

        audio_data = np.concatenate(self._audio_frames, axis=0)
        print(f"🎧 Recorded {len(audio_data) / self.samplerate:.2f} seconds of audio.")
        return audio_data


# 🔹 Example usage (standalone test)
if __name__ == "__main__":
    model = RecordModel()

    # Start recording for 5 seconds
    model.start_recording(max_seconds=5)

    # Optionally stop manually earlier
    # time.sleep(3)
    # model.stop_recording()

    # Wait for thread to finish
    time.sleep(6)

    # Retrieve data
    audio = model.get_audio_data()

    # Playback for verification
    if len(audio) > 0:
        sd.play(audio, model.samplerate)
        sd.wait()
