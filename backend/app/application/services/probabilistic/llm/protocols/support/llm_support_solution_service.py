from app.application.services.probabilistic.llm.client.llm_client import LLMClient
from app.application.services.probabilistic.llm.domain.llm import LLMSolution
from app.application.services.probabilistic.llm.utils.llm_call import call_llm_json
from app.application.solution_service import SolutionService
from app.domain.workflow import Solution, WorkflowContext


class LLMSupportSolutionService(SolutionService):
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
            You are a troubleshooting assistant.
            You already have all information provided by the user.

            Your task:
            - Provide the best possible solution given the ticket data, previous solution (if exists)
              and the information provided by the user.
              This field should not be null or empty.
              If the current solution already satisfies the feedback, you may return an improved
              but equivalent version rather than inventing new content.
            - Specify a confidence level between 0.0 and 1.0 for your solution.
            - Provide a brief rationale for your solution.
              This field can be null if not applicable.

            Provide the best possible solution based on available information.
            If information is incomplete, state assumptions explicitly.

            Guidance for solution_confidence:
            - 1.0 = complete certainty
            - 0.5 = partial confidence
            - <0.3 = weak confidence

            Return ONLY valid JSON matching this schema:

            {{
                "content": string,
                "solution_confidence": number between 0.0 and 1.0,
                "rationale": string or null
            }}

            Rules:
            - Write the solution in Markdown. Include explanations, step-by-step instructions, code snippets as needed.
            - Write the rationale in one plain-text sentence without Markdown.
            - Do NOT include text outside JSON.

            Context:
            TICKET TITLE:
            {ctx.ticket.title}

            TICKET DESCRIPTION:
            {ctx.ticket.description}

            CLARIFICATION ANSWERS FROM USER:
            {answered_block}

            CURRENT PROPOSED SOLUTION:
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
