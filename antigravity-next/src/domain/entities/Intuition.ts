// src/domain/entities/Intuition.ts

export interface IntuitionProps {
  id?: string;
  pattern: string;
  category: string;
  confidence: number;
  userId: string;
  createdAt?: Date;
}

export class Intuition {
  constructor(public readonly props: IntuitionProps) {
    if (props.confidence < 0 || props.confidence > 1) {
      throw new Error("Confidence must be between 0 and 1");
    }
  }
}
