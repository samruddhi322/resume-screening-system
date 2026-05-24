from src.preprocessing import extract_text_from_pdf, clean_text, remove_stopwords

resume_text = extract_text_from_pdf("data/sample_resume.pdf")

cleaned_text = clean_text(resume_text)

final_text = remove_stopwords(cleaned_text)

print(final_text)