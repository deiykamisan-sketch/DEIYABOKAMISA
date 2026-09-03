import tempfile
from pathlib import Path
import cv2
import numpy as np
from django.test import SimpleTestCase
from camera.detector import ColorMarkerDetector
from pen_tracking.tracker import PenTracker
from whiteboard.drawing import DrawingLayer
from speech.voice_commands import parse_command
from ai.summarizer import summarize
from ai.notes import build_notes
from ai.pdf_generator import create_lecture_pdf

class AirBoardCoreTests(SimpleTestCase):
    def test_green_pen_marker_detection(self):
        frame=np.zeros((240,320,3),dtype=np.uint8);cv2.circle(frame,(160,120),18,(0,255,0),-1)
        detection,_=ColorMarkerDetector().detect(frame)
        self.assertIsNotNone(detection);self.assertLess(abs(detection.x-160),3);self.assertLess(abs(detection.y-120),3)

    def test_tracker_smooths_points(self):
        class D: pass
        tracker=PenTracker(smoothing=2)
        a=D();a.x=10;a.y=10;b=D();b.x=20;b.y=20
        tracker.update(a);self.assertEqual(tracker.update(b),(15,15))

    def test_transparent_drawing_composite(self):
        layer=DrawingLayer(100,100);layer.draw((10,10));layer.draw((90,90))
        output=layer.composite(np.zeros((100,100,3),dtype=np.uint8))
        self.assertGreater(int(output.sum()),0)

    def test_arabic_voice_command(self):
        self.assertEqual(parse_command('من فضلك امسح السبورة'),'clear')

    def test_summary_and_pdf(self):
        transcript='Networks connect devices. A switch connects local devices. A router connects networks.'
        notes=build_notes('Computer Networks',transcript)
        self.assertTrue(summarize(transcript))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'lecture.pdf';create_lecture_pdf(path,notes)
            self.assertTrue(path.exists());self.assertGreater(path.stat().st_size,100)
