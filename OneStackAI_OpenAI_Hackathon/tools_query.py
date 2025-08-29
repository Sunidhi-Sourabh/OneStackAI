from tools import tools_data

def get_tools_by_category(category):
    normalized = category.strip().lower()
    for key in tools_data:
        if key.strip().lower() == normalized:
            return tools_data[key]
    return []

def get_tools_by_keyword(keyword):
    keyword = keyword.lower()
    results = []
    for category_tools in tools_data.values():
        for tool in category_tools:
            if keyword in tool.get("Description", "").lower():
                results.append(tool)
    return results

def get_tools_by_feature(feature):
    feature = feature.lower()
    results = []
    for category_tools in tools_data.values():
        for tool in category_tools:
            if feature in tool.get("Tool Name", "").lower() or feature in tool.get("Description", "").lower():
                results.append(tool)
    return results

def get_tools_by_category_and_pricing(category, pricing):
    category = category.strip().lower()
    pricing = pricing.strip().lower()
    for key in tools_data:
        if key.strip().lower() == category:
            return [tool for tool in tools_data[key] if tool.get("Free/Paid", "").lower() == pricing]
    return []

# Optional: Debug test block
if __name__ == "__main__":
    print("[✅] Testing get_tools_by_category('marketing & branding'):")
    tools = get_tools_by_category("marketing & branding")
    for tool in tools[:3]:
        print("-", tool["Tool Name"])

    print("\n[✅] Testing get_tools_by_feature('voice'):")
    tools = get_tools_by_feature("voice")
    for tool in tools[:3]:
        print("-", tool["Tool Name"])

    print("\n[✅] Testing get_tools_by_category_and_pricing('marketing & branding', 'free'):")
    tools = get_tools_by_category_and_pricing("marketing & branding", "free")
    for tool in tools:
        print("-", tool["Tool Name"])
