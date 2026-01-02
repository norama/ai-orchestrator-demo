from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.domain.llm import LLMAction, LLMNextStep
from app.application.services.probabilistic.llm.utils.llm_call import call_llm_json
from app.application.step_generator import StepGenerator
from app.domain.workflow import ClarificationStep, NextStepDecision, WorkflowContext


class LLMReportStepGenerator(StepGenerator):
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    @staticmethod
    def _build_prompt(ctx: WorkflowContext) -> str:
        answered = [
            f"{i + 1} \n Q: {s.prompt} \n A: {s.answer} \n" for i, s in enumerate(ctx.steps) if s.answer is not None
        ]

        answered_block = "\n".join(answered) if answered else "(none)"

        return f"""
            You are preparing to generate a written REPORT.

            Your task:
            - Decide whether another clarification question is needed before writing the report.
            - Ask AT MOST one clarification question.
            - Prefer stopping early if the report can reasonably be drafted.

            Clarification guidance:
            - Typical useful clarifications include: audience, length, focus.
            - Do NOT ask about templates, formatting, or export options.

            IMPORTANT:
            If the ticket description does NOT contain concrete factual information
            (e.g. progress, completed work, findings, metrics),
            you MUST ask the user to provide a brief factual status summary
            before generating the report.
            Example clarification:
            "What is the current factual status of the project (completed work, current phase, known issues)?"

            When unsure AND factual information is missing, prefer action = "ASK" over "DONE".

            Return ONLY valid JSON matching this schema:

            {{
                "action": "ASK" | "DONE",
                "prompt": string | null,
                "workflow_confidence": number between 0.0 and 1.0,
                "reason": string
            }}

            Rules:
            - If action is "ASK", prompt MUST be non-empty.
            - If action is "DONE", prompt MUST be null.
            - No markdown, no explanations, no text outside JSON.

            Context:
            REPORT TITLE:
            {ctx.ticket.title}

            REPORT DESCRIPTION:
            {ctx.ticket.description}

            CLARIFICATION ANSWERS SO FAR:
            {answered_block}

            MAX STEPS: {ctx.max_steps}
            STEPS USED: {len(ctx.steps)}
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
