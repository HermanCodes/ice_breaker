from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import person_intel_parser, PersonIntel
from third_parties.linkedin import scrape_linkedin_profile, scrape_linkedin_profile_test

from dotenv import load_dotenv

load_dotenv()


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    # linkedin_data = scrape_linkedin_profile_test(name=name)

    summary_template = """
            given the following Linkedin information {information} about a person, I want you to create:
            1. a short summary of the person
            2. numbered list of two interesting facts about the person
            3. A topic that may interest them
            4. 2 creative Ice breakers to open up a conversation with them
            \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = AzureChatOpenAI(
        deployment_name="RegMarketGpt35Turbo",
        temperature=0,
    )

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    with get_openai_callback() as cb:
        result = chain.run(information=linkedin_data)
        print(result)
        print(f"Total Cost (USD): ${format(cb.total_cost, '.6f')}")

    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello, LangChain!")
    result = ice_break(name="Neha Shawrikar")
