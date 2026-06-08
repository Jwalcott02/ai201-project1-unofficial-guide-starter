# The Unofficial Guide — Project 1

**Demo Video:** <div>
    <a href="https://www.loom.com/share/a66042d93af84a04a208571dbb56ab03">
      <p>Loom Message - 8 June 2026 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/a66042d93af84a04a208571dbb56ab03">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/a66042d93af84a04a208571dbb56ab03-4c163cd66d53ae34-full-play.gif#t=0.1">
    </a>
  </div>

---

## Domain

Student-generated knowledge about FAU Computer Science professors and degree requirements. FAU's official channels tell you nothing about what a professor's exams are actually like, how heavy the workload is, or how clearly they explain concepts. This knowledge exists scattered across Rate My Professors but is not searchable or synthesized anywhere — students have to manually dig through posts before every registration period. This system makes that knowledge answerable through plain-language questions.

---

## Document Sources

| # | Source | Description | URL or file path |
|---|--------|-------------|-----------------|
| 1 | Sareh Taebi | RMP professor reviews | ratemyprofessors.com/professor/2531409 |
| 2 | Safak Kayikci | RMP professor reviews | ratemyprofessors.com/professor/2977967 |
| 3 | Juan Yepes | RMP professor reviews | ratemyprofessors.com/professor/2950560 |
| 4 | Maria Petrie | RMP professor reviews | ratemyprofessors.com/professor/1347714 |
| 5 | Mehrdad Nojoumian | RMP professor reviews | ratemyprofessors.com/professor/2031921 |
| 6 | Baseem Alhalabi | RMP professor reviews | ratemyprofessors.com/professor/647877 |
| 7 | Ali Ibrahim | RMP professor reviews | ratemyprofessors.com/professor/2832618 |
| 8 | FAU CS Program Summary | Official degree requirements and course listing | fau.edu/engineering/eecs/undergraduate/computer-science/program-sumary-bscs/ |
| 9 | COP3530 Syllabus | Official course syllabus — Data Structures | documents/cop3530data-structures-algorithm-analysis.pdf |
| 10 | COT4400 Syllabus | Official course syllabus — Algorithms | documents/cot4400design-analysis-algorithms.pdf |
| 11 | COP4610 Syllabus | Official course syllabus — Operating Systems | documents/cop4610computer-op-systems.pdf |

---

## Chunking Strategy

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**
My corpus has two types of documents with different structures. RMP professor reviews are short and self-contained (3-6 sentences each), so 500 characters keeps most individual reviews intact as single chunks, preserving the full context of one student opinion. Splitting mid-review would lose the connection between a student complaint and the course they were describing. For the syllabus PDFs and program summary, 500 characters captures individual sections like prerequisites or topic lists without merging unrelated content together. A 50-character overlap ensures that information near chunk boundaries is not lost. Chunks that are too small would fragment individual reviews into meaningless phrases. Chunks that are too large would merge multiple reviews together, making it hard to attribute a specific opinion to a specific course or professor.

**Final chunk count:** 73

---

## Sample Chunks

| # | Source | Chunk |
|---|--------|-------|
| 1 | petrie_maria.txt | Quality: 1.0 - Course: CDA3203 - Apr 21 2026: Started off easy, but somewhere in the middle started giving a million quizzes even if material was covered poorly. Quiz questions often have no partial credit, just big 0s. |
| 2 | nojoumian_mehrdad.txt | Professor Nojoumian may seem strict and serious at first, but he genuinely cares that students understand data structures and algorithm analysis for job interviews and careers. Attendance and participation count as extra credit. |
| 3 | ibrahim_ali.txt | No tests, one quiz, rest all homework. Really cares that you understand the topic. Helpful during office hours. Records lectures on Zoom. Homework was real-life scenario problems. |
| 4 | cop3530data-structures-algorithm-analysis.pdf | Prerequisites: COP 3014. Corequisites: MAD 2104. Required. Topics include linked lists, stacks, queues, trees, sorting algorithms, and graph ADT. |
| 5 | fau_cs_program_summary.txt | COMPUTER SCIENCE CORE (Required): Introduction to Database Structures (COP 3540), Principles of Programming Languages (COP 4020), Design and Analysis of Algorithms (COT 4400), Theory of Computation (COT 4420) |

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
For a production system I would consider OpenAI text-embedding-ada-002 for higher accuracy on domain-specific text, but it costs money per token and requires an API key. all-MiniLM-L6-v2 runs locally with no cost or rate limits, which fits this project. Context length and multilingual support are not concerns here since all documents are English and relatively short.

---

## Retrieval Test Results

**Query 1: What should I know before taking Professor Petrie?**
Top chunks returned from: petrie_maria.txt (distance: 0.670)
Relevant because: The chunk contains direct student warnings about unannounced quizzes, no partial credit, and disorganized lectures — exactly what a student needs to know before enrolling.

**Query 2: What are the prerequisites for COT4400 Algorithms?**
Top chunks returned from: cot4400design-analysis-algorithms.pdf (distance: 1.086)
Relevant because: The syllabus PDF chunk contains the exact prerequisites section stating Prerequisites: COP 3530 — directly answering the question from an official source.

**Query 3: Who should I take for Data Mining at FAU?**
Top chunks returned from: ibrahim_ali.txt (distance: 0.797)
Relevant because: The chunk contains Ibrahim profile showing he teaches CAP4770 Data Mining and Machine Learning with a 4.2 rating and positive reviews about his teaching style.

---

## Grounded Generation

**System prompt grounding instruction:** Answer the question using ONLY the information provided in the documents below. Do not use any outside knowledge or general information. If the documents do not contain enough information to answer the question, say exactly: I do not have enough information in my documents to answer that.

**How source attribution is surfaced in the response:** Source filenames are collected from ChromaDB metadata for each retrieved chunk and displayed programmatically in the Retrieved From field of the Gradio interface after every response.

---

## Example Responses

**Query 1: What should I know before taking Professor Petrie?**
Response: Before taking Professor Petrie, you should know that she is considered disorganized by many students. Her lectures can be boring and hard to follow, with random quizzes given with no warning or study prep time. Quiz questions often have no partial credit. However, she does care about her students learning and will help if you ask and attend lectures.
Retrieved from: petrie_maria.txt

**Query 2: What are the prerequisites for COT4400 Algorithms?**
Response: The prerequisites for COT 4400 Design and Analysis of Algorithms is COP 3530, which is Data Structures and Algorithm Analysis. (Specific course information, section b. Prerequisites: COP 3530)
Retrieved from: cot4400design-analysis-algorithms.pdf

**Out-of-scope query: What is the best restaurant near FAU?**
Response: I do not have enough information in my documents to answer that.
Retrieved from: N/A — system correctly refused to answer outside its document scope.

---

## Query Interface

The system uses a Gradio web UI accessible at http://127.0.0.1:7860. It has the following fields:

- Your Question (text input): The user types a plain-language question about FAU CS professors, courses, or degree requirements.
- Answer (text output): The system returns a grounded response generated by Groq llama-3.3-70b-versatile using only the retrieved chunks as context.
- Retrieved From (text output): Lists the source document filenames that were used to generate the answer.

**Sample interaction transcript:**

User: Who should I take for Data Mining at FAU?

Answer: According to the documents, Professor Ali Ibrahim teaches CAP4770, which is Introduction to Data Mining and Machine Learning. He has an overall rating of 4.2/5 and 75% of students would take him again. A review states he explains everything step by step and is always willing to help. Based on the provided information, Professor Ali Ibrahim seems like a good option for Data Mining at FAU.

Retrieved from: ibrahim_ali.txt, taebi_sareh.txt, kayikci_safak.txt

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are Professor Taebi exams like? | Midterms difficult, average 50%, mostly coding problems, final easier | System said it did not have enough information, only found one vague reference to her being a very interesting test proctor | Partially relevant | Inaccurate |
| 2 | What should I know before taking Professor Petrie? | Frequent unannounced quizzes, no partial credit, disorganized lectures | Accurately described disorganized quizzes, hard to follow lectures, but also noted she cares about students | Relevant | Accurate |
| 3 | Who should I take for Data Mining at FAU? | Professor Ibrahim, project-based, no tests | Correctly identified Ibrahim, cited 4.2 rating and step-by-step teaching style | Relevant | Accurate |
| 4 | What are the prerequisites for COT4400 Algorithms? | COP3530 Data Structures | Correctly cited COP 3530 with direct reference to syllabus section | Relevant | Accurate |
| 5 | What courses are required for the FAU CS degree? | 120 credits, core courses listed | Accurately listed mathematics, common core, and CS core requirements with course numbers | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** What are Professor Taebi exams like?

**What the system returned:** I do not have enough information in my documents to answer that. The documents only mention that Professor Taebi is a very interesting test proctor in one review for COP3410.

**Root cause (tied to a specific pipeline stage):** Chunking stage. The Taebi document was split into fixed-size chunks of 500 characters. The chunk retrieved by the query contained the professor header and first review, which mentioned her as a test proctor but contained no exam details. The actual exam information — midterm averages of 50%, coding-heavy questions, easier finals — was spread across later chunks that scored lower in semantic similarity search because they did not prominently mention Taebi and exams together in the same chunk.

**What you would change to fix it:** Chunk by individual review rather than fixed character count. Each review is a self-contained unit of meaning — if each review were its own chunk, the retrieval would find the specific reviews mentioning exam difficulty rather than the header chunk.

---

## Spec Reflection

**One way the spec helped you during implementation:** The spec requirement to write evaluation questions before coding forced me to think concretely about what the system needed to do. This directly shaped which professors and documents I collected — I needed sources that could actually answer my 5 questions.

**One way your implementation diverged from the spec, and why:** The spec suggested scraping live URLs, but Rate My Professors blocks automated requests due to JavaScript rendering. I manually copied review text into structured txt files instead. This was slower but produced cleaner documents with consistent formatting that chunked more predictably.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My chunking strategy section, document file structure, and pipeline diagram from planning.md
- *What it produced:* ingest.py with load_txt, load_pdf, clean_text, chunk_text functions and ChromaDB storage code
- *What I changed or overrode:* Verified chunk sizes matched my 500/50 spec, added extra reviews to professor files when chunks were too sparse for retrieval

**Instance 2**

- *What I gave the AI:* My retrieval approach section and grounding requirement from the spec
- *What it produced:* query.py with retrieve and ask functions, system prompt enforcing grounding, and app.py Gradio interface
- *What I changed or overrode:* Changed the placeholder example question, updated the UI colors to match FAU navy and red branding, switched from dark to light theme
