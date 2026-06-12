"""Capa model: lógica lingüística del detector. No conoce HTTP ni FastAPI."""
from model.detector import analyze_text, analyze_sentence

__all__ = ["analyze_text", "analyze_sentence"]
