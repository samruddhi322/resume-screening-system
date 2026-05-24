from src.matcher import calculate_similarity

resume = """
python sql machine learning pandas tensorflow
"""

job_description = """
looking for python developer with sql and machine learning experience
"""

score = calculate_similarity(resume, job_description)

print("Similarity Score:", score)