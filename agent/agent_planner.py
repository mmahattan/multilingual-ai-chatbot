class AgentPlanner:
    def __init__(self, model, tools):
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.tool_descriptions = "\n".join([
            f"- {tool.name}: {tool.description}" for tool in tools
        ])

    def plan(self, query, context):
        prompt = (
            "You are the KTB Client Zero AI Agent.\n"
            "Your job is to classify the user query into exactly one of these 5 tools:\n\n"
            "- new_operating_model: questions about AI-orchestrated enterprises, siloed IT, operating model\n"
            "- new_ways_of_working: questions about human-agent collaboration, linear delivery, team workflows\n"
            "- it_capability_uplift: questions about IT pipelines, agent platforms, technology infrastructure\n"
            "- talent_workforce: questions about reskilling, developers, builders, orchestrators, workforce, people, talent\n"
            "- change_management: questions about AI-native culture, adoption, transformation, mindset\n\n"
            "Rules:\n"
            "- Return ONLY the tool name\n"
            "- Do not explain\n"
            "- Do not add punctuation\n\n"
            "Examples:\n"
            "Query: How is KTB reskilling its developers? -> talent_workforce\n"
            "Query: How is KTB building AI culture? -> change_management\n"
            "Query: How are IT pipelines upgraded? -> it_capability_uplift\n\n"
            "Query: " + query + "\n"
            "Tool:"
        )
        result    = self.model.generate_text(prompt=prompt)
        tool_name = result.strip().lower().split()[0]
        return tool_name if tool_name in self.tools else "new_operating_model"

    def act(self, tool_name, query, language):
        return self.tools[tool_name].run(query, language)