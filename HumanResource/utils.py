import os
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()


def get_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_data(job, cv_path):
    resume = get_text(pdf_path=cv_path)

    responsibilities = ''.join(job.responsibilities.split('\n'))
    qualifications = ''.join(job.qualifications.split('\n'))

    data = {'resume': resume, 'responsibilities': responsibilities, 'qualifications': qualifications}

    return data


def consult_ai(job, cv_path):

    data = get_data(job=job, cv_path=cv_path)

    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": f"""You are an experienced HR assistant. We are shortlisting candidates for a job in the
                 company. Given a resume, job responsibilities and required qualifications you are supposed to rate that \
                 resume in a scale of 0 to 100 percent where 0 is lowest score and 100 is highest score.
                 This is is the resume: {data['resume']}
                 This are the responsibilities: {data['responsibilities']}
                 This are the qualifications: {data['qualifications']}
                    
                 return your response in a python dictionary format with score and summary as keys
                 NOTE: return dictionary output only i.e respond like and API
                 """
            },
            {
                "role": "assistant",
                "content": "" 
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    data = ''

    for chunk in completion:
        try:
            data += chunk.choices[0].delta.content
        except Exception as e:
            pass

    data = data.replace("\'", "\"")

    return data

