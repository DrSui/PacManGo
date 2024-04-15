from gemini import Gemini
GeminiClient = Gemini(cookies = {'CONSENT': 'YES+srp.gws-20210929-0-RC1.en+FX+902', 'AEC': 'AakniGPlA9YV9GVqY-4SRorPPk42fmEqFv7HM84jx1PQSEyjMxTNYp982kU', '1P_JAR': '2022-09-25-22', 'NID': '511=bwzvhUDkmaorOisVHzTsXZ4gtJ9Y0f0tdxVsZ8AFicfqw06l_amipeqFjNtL673g-uK3AjPg27xfmJ_QWa5jFBFyjxTCWrIW40Na3ojv-zsOzTXOYkQXQiiWoESkyryjaUcKxmaVvkRxLL1FFGlZ6K5mnP-LWqCl3h_JgXGHI_s'})

# Testing needed as cookies vary by region.
# GeminiClient = Gemini(auto_cookies=True, target_cookies=["__Secure-1PSID", "__Secure-1PSIDTS"])
# GeminiClient = Gemini(auto_cookies=True, target_cookies="all") # You can pass whole cookies

response = GeminiClient.generate_content("Hello, Gemini. What's the weather like in Seoul today?")
print(response.payload)
