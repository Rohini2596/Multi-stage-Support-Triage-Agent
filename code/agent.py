from __future__ import annotations
from code.pipeline import SupportPipeline
class SupportAgent:
    def __init__(self):
        self.pipeline = SupportPipeline()
    def run(self, df):
        return [self.pipeline.process_row(row.to_dict()) for _, row in df.iterrows()]
