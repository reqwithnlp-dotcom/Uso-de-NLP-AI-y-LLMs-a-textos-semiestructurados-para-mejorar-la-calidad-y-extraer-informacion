import pandas as pd
import numpy as np
import spacy
import textdescriptives as td
import fastapi as fa


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textdescriptives/readability")

text = "The committee, during a long meeting, reviewed the regional funding proposal and approved a preliminary schedule for implementation. The report, which described budget constraints and administrative delays and expected benefits for local institutions, guided the discussion. Several members, asking for clearer deadlines and stronger monitoring and a public summary for citizens, supported the plan. The final decision, keeping the original objective, required each department to submit progress information every month."

doc = nlp(text)

print(doc._.readability)