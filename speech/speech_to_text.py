"""Provider-neutral transcript accumulator; browser recognition supplies segments in the MVP."""
from dataclasses import dataclass,field
from datetime import datetime,timezone
@dataclass
class Transcript:
    segments:list=field(default_factory=list)
    def add(self,text,speaker='Lecturer'):
        cleaned=' '.join(text.split())
        if cleaned:self.segments.append({'speaker':speaker,'text':cleaned,'time':datetime.now(timezone.utc).isoformat()})
    def plain_text(self): return '\n'.join(f"{x['speaker']}: {x['text']}" for x in self.segments)
