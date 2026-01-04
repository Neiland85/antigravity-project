// src/domain/repositories/IIntuitionRepository.ts
import { Intuition } from "../entities/Intuition";

export interface IIntuitionRepository {
  save(intuition: Intuition): Promise<void>;
  findByUser(userId: string): Promise<Intuition[]>;
}
