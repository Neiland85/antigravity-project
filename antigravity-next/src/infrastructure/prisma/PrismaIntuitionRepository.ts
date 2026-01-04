// src/infrastructure/prisma/PrismaIntuitionRepository.ts
import { PrismaClient } from "@prisma/client";
import { Intuition } from "../../domain/entities/Intuition";
import { IIntuitionRepository } from "../../domain/repositories/IIntuitionRepository";

export class PrismaIntuitionRepository implements IIntuitionRepository {
  private prisma: PrismaClient;

  constructor() {
    this.prisma = new PrismaClient();
  }

  // To support RLS, we wrap the client to set the session user
  private async setSessionUser(userId: string) {
    await this.prisma.$executeRawUnsafe(`SET app.current_user = '${userId}'`);
  }

  async save(intuition: Intuition): Promise<void> {
    const { pattern, category, confidence, userId } = intuition.props;

    // Setting user identity for RLS audit or policy if needed
    await this.setSessionUser(userId);

    await this.prisma.intuition.create({
      data: {
        pattern,
        category,
        confidence,
        userId,
      },
    });
  }

  async findByUser(userId: string): Promise<Intuition[]> {
    await this.setSessionUser(userId);

    const records = await this.prisma.intuition.findMany({
      where: { userId }, // Basic filtering, though RLS would enforce this at DB level
    });

    return records.map(
      (r) =>
        new Intuition({
          id: r.id,
          pattern: r.pattern,
          category: r.category,
          confidence: r.confidence,
          userId: r.userId,
          createdAt: r.createdAt,
        })
    );
  }
}
