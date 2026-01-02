from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.domain.llm import LLMAction, LLMNextStep
from app.application.services.probabilistic.llm.utils.llm_call import call_llm_json
from app.application.step_generator import StepGenerator
from app.domain.workflow import ClarificationStep, NextStepDecision, WorkflowContext


class LLMSupportStepGenerator(StepGenerator):
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    @staticmethod
    def _build_prompt(ctx: WorkflowContext) -> str:
        answered = [f"- Q: {s.prompt}\n  A: {s.answer}" for s in ctx.steps if s.answer is not None]

        answered_block = "\n".join(answered) if answered else "- (none)"

        return f"""
            You are a troubleshooting assistant.

            Your task:
            - Decide whether another clarification question is needed.
            - Ask AT MOST one clarification question.
            - If enough information is available, stop asking questions.

            When deciding whether to ask another question:
            - Consider how many steps are still available.
            - If you are unsure whether another question will materially improve the solution,
              prefer returning action = "DONE" with lower confidence.

            Guidance for workflow_confidence:
            - 1.0 = complete certainty
            - 0.5 = partial confidence
            - <0.3 = weak confidence


            Return ONLY valid JSON matching this schema:

            {{
                "action": "ASK" | "DONE",
                "prompt": string | null,
                "workflow_confidence": number between 0.0 and 1.0,
                "reason": string
            }}

            Rules:
            - If action is "ASK", prompt MUST be a non-empty string.
            - If action is "DONE", prompt MUST be null.
            - Do NOT include explanations.
            - Do NOT include Markdown.
            - Do NOT include text outside JSON.

            Context:
            TICKET TITLE:
            {ctx.ticket.title}

            TICKET DESCRIPTION:
            {ctx.ticket.description}

            CLARIFICATION ANSWERS SO FAR:
            {answered_block}

            MAX STEPS ALLOWED: {ctx.max_steps}
            STEPS TAKEN SO FAR: {len(ctx.steps)}
        """.strip()

    def propose_next(self, ctx: WorkflowContext) -> NextStepDecision:
        prompt = self._build_prompt(ctx)

        try:
            data = call_llm_json(self.llm, prompt)
            next_llm_step = LLMNextStep.model_validate(data)
            next_llm_step = LLMNextStep.validate_semantics(next_llm_step)

        except Exception as e:
            # Safe fallback — never crash the engine
            return NextStepDecision(
                next_step=None,
                workflow_confidence=0.3,
                reason=f"LLM failure, falling back safely: {e}",
            )

        if next_llm_step.action == LLMAction.ASK:
            assert next_llm_step.prompt is not None

            return NextStepDecision(
                next_step=ClarificationStep(prompt=next_llm_step.prompt),
                workflow_confidence=next_llm_step.workflow_confidence,
                reason=next_llm_step.reason,
            )

        return NextStepDecision(
            next_step=None,
            workflow_confidence=next_llm_step.workflow_confidence,
            reason=next_llm_step.reason,
        )
