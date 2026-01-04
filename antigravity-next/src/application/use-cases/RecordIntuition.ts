// src/application/use-cases/RecordIntuition.ts
import { Intuition } from "../../domain/entities/Intuition";
import { IIntuitionRepository } from "../../domain/repositories/IIntuitionRepository";

interface RecordIntuitionRequest {
  pattern: string;
  category: string;
  confidence: number;
  userId: string;
}

export class RecordIntuition {
  constructor(private intuitionRepository: IIntuitionRepository) {}

  async execute(request: RecordIntuitionRequest): Promise<void> {
    const intuition = new Intuition({
      pattern: request.pattern,
      category: request.category,
      confidence: request.confidence,
      userId: request.userId,
    });

    await this.intuitionRepository.save(intuition);
  }
}
