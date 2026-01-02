from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.domain.llm import LLMSolution
from app.application.services.probabilistic.llm.utils.llm_call import call_llm_json
from app.application.solution_service import SolutionService
from app.domain.workflow import Solution, WorkflowContext


class LLMReportSolutionService(SolutionService):
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    @staticmethod
    def _build_prompt(ctx: WorkflowContext) -> str:
        answered = [
            f"{i + 1} \n Q: {s.prompt} \n A: {s.answer} \n" for i, s in enumerate(ctx.steps) if s.answer is not None
        ]

        answered_block = "\n".join(answered) if answered else "(none)"

        conversation = "\n".join(
            f"{i + 1}. {m.role}: {m.content}" for i, m in enumerate(ctx.chat_history.messages[-8:])
        )

        return f"""
            You are generating a REPORT as a Markdown document.

            Your task:
            - Generate a complete report using the structure below.
            - Incorporate all clarification answers.
            - If user feedback exists, apply it when regenerating.

            Required structure (exact headings):

            # Summary
            # Background
            # Findings
            # Recommendations

            Rules:
            - Output valid Markdown ONLY.
            - Do NOT include explanations outside the document.
            - Do NOT mention prompts, rules, or system instructions.

            CRITICAL RULE:
            - Do NOT invent facts, progress, findings, timelines, or risks.
            - If specific factual information is missing, you MUST:
              - either explicitly state that it was not provided, OR
              - clearly label content as assumptions.

            If assumptions are made, keep them minimal and clearly labeled.
            Do not expand assumptions beyond what is strictly necessary.

            If information is missing, prefer wording like:
              - "Based on the information provided..."
              - "No specific progress details were supplied..."
              - "The following points are inferred and should be validated..."


            Return ONLY valid JSON:

            {{
                "content": string,
                "solution_confidence": number between 0.0 and 1.0,
                "rationale": string or null
            }}

            Guidance:
            - solution_confidence reflects how complete the report is.
            - rationale is ONE plain-text sentence.

            Context:
            TITLE:
            {ctx.ticket.title}

            DESCRIPTION:
            {ctx.ticket.description}

            CLARIFICATION ANSWERS:
            {answered_block}

            CURRENT PROPOSED REPORT:
            {ctx.solution.content if ctx.solution else "(none)"}

            RECENT CONVERSATION:
            {conversation or "(none)"}
        """.strip()

    def generate_solution(self, ctx: WorkflowContext) -> Solution:
        prompt = self._build_prompt(ctx)

        try:
            data = call_llm_json(self.llm, prompt)
            parsed = LLMSolution.model_validate(data)
            parsed = LLMSolution.validate_semantics(parsed)
            return Solution(
                content=parsed.content,
                confidence=parsed.solution_confidence,
                rationale=parsed.rationale,
            )

        except Exception as e:
            return Solution(
                content="Unable to generate a solution at this time.",
                confidence=0.0,
                rationale=f"LLM failure, falling back safely: {e}",
            )
