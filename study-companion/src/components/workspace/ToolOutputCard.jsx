import { useState, useEffect } from "react";
import api from "@/lib/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ToolOutputCard({ activeId, notebookId }) {
  // Tutor (Explain) state - hardcoded value
  const tutorQuery = "Explain the concept of [topic] in simple terms with examples.";
  const [tutorData, setTutorData] = useState(null);
  const [tutorLoading, setTutorLoading] = useState(false);

  const submitTutor = async () => {
    setTutorLoading(true);
    try {
      const res = await api.post(`/notebooks/${notebookId}/tutor/`, { query: tutorQuery });
      setTutorData(res.data);
    } finally {
      setTutorLoading(false);
    }
  };

  // Quiz state
  const [quizQuery, setQuizQuery] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [quizLoading, setQuizLoading] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [answered, setAnswered] = useState({});

  const submitQuiz = async () => {
    setQuizLoading(true);
    try {
      const res = await api.post(`/notebooks/${notebookId}/quiz/`, { query: quizQuery });
      setQuizData(res.data);
    } finally {
      setQuizLoading(false);
    }
  };

  const submitAnswer = async (quizId, questionId) => {
    const answer = selectedAnswers[questionId];
    if (!answer) return;
    const res = await api.post(`/notebooks/quizzes/${quizId}/questions/${questionId}/answer/`, { answer });
    setAnswered((prev) => ({ ...prev, [questionId]: res.data }));
  };

  // Plan state
  const [planQuery, setPlanQuery] = useState("");
  const [planData, setPlanData] = useState(null);
  const [planLoading, setPlanLoading] = useState(false);

  const submitPlan = async () => {
    setPlanLoading(true);
    try {
      const res = await api.post(`/notebooks/${notebookId}/study-plan/`, { query: planQuery });
      setPlanData(res.data);
    } finally {
      setPlanLoading(false);
    }
  };

  // Research state
  const [researchQuery, setResearchQuery] = useState("");
  const [researchData, setResearchData] = useState(null);
  const [researchLoading, setResearchLoading] = useState(false);

  const submitResearch = async () => {
    setResearchLoading(true);
    try {
      const res = await api.post(`/notebooks/${notebookId}/research/`, { query: researchQuery });
      setResearchData(res.data);
    } finally {
      setResearchLoading(false);
    }
  };

  // Progress state
  const [progressData, setProgressData] = useState(null);
  const [progressLoading, setProgressLoading] = useState(false);
  const [progressExpanded, setProgressExpanded] = useState(false);

  useEffect(() => {
    if (activeId !== "progress" || progressData) return;
    const fetchProgress = async () => {
      setProgressLoading(true);
      try {
        const res = await api.post(`/notebooks/${notebookId}/progress/`, {});
        setProgressData(res.data);
      } finally {
        setProgressLoading(false);
      }
    };
    fetchProgress();
  }, [activeId, notebookId, progressData]);

  return (
    <div className="mt-4 p-8 rounded-lg bg-brick/10">
      {/* Tutor Tab - Read-only textarea with hardcoded text */}
      {activeId === "explain" && (
        <div>
          <textarea
            value={tutorQuery}
            readOnly
            disabled
            rows={6}
            className="w-full px-3 py-2 rounded-md border border-teal text-sm text-oxblood bg-cream/60 cursor-not-allowed resize-none opacity-80"
          />
          <button
            onClick={submitTutor}
            disabled={tutorLoading}
            className="mt-2 px-4 py-2 rounded-md bg-burnt text-teal text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {tutorLoading ? "Tutoring..." : "Explain"}
          </button>

          {tutorLoading && (
            <div className="mt-4 space-y-3 animate-pulse">
              <div className="h-16 rounded-lg bg-brick/20" />
              <div className="h-16 rounded-lg bg-brick/20" />
              <div className="h-16 rounded-lg bg-brick/20" />
            </div>
          )}

          {!tutorLoading && tutorData && (
            <div className="mt-4 p-4 rounded-lg bg-cream/40 border border-teal/20">
              <p className="text-sm text-oxblood whitespace-pre-wrap">
                {tutorData.explanation || tutorData.response || JSON.stringify(tutorData)}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Quiz Tab */}
      {activeId === "test" && (
        <div>
          <input
            value={quizQuery}
            onChange={(e) => setQuizQuery(e.target.value)}
            placeholder="Topic to quiz on..."
            className="w-full px-3 py-2 rounded-md border border-teal text-sm text-oxblood placeholder:text-oxblood/70 focus:outline-none focus:ring-2 focus:ring-teal/40"
          />
          <button
            onClick={submitQuiz}
            disabled={quizLoading || !quizQuery.trim()}
            className="mt-2 px-4 py-2 rounded-md bg-burnt text-teal text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {quizLoading ? "Generating..." : "Generate Quiz"}
          </button>

          {quizLoading && (
            <div className="mt-4 space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-20 rounded-lg bg-brick/20" />
              ))}
            </div>
          )}

          {!quizLoading && !quizData && (
            <p className="mt-4 text-sm text-oxblood/70">
              Enter a topic above and generate a quiz to test yourself.
            </p>
          )}

          {!quizLoading && quizData?.questions?.length > 0 && (
            <div className="mt-4 space-y-5">
              {quizData.questions.map((q) => (
                <div key={q.id}>
                  <p className="text-sm font-medium text-oxblood mb-2">
                    {q.order}. {q.question_text}
                  </p>
                  <div className="grid gap-2">
                    {q.options.map((opt, i) => {
                      const isSelected = selectedAnswers[q.id] === opt;
                      return (
                        <button
                          key={i}
                          onClick={() =>
                            setSelectedAnswers((prev) => ({ ...prev, [q.id]: opt }))
                          }
                          disabled={!!answered[q.id]}
                          className={`text-left px-3 py-2 rounded-md border text-sm transition-colors
                            ${isSelected
                              ? "border-teal bg-teal/10 text-teal font-medium"
                              : "border-brick/20 text-oxblood hover:bg-cream/60 hover:border-teal/40"
                            }`}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>

                  {!answered[q.id] ? (
                    <button
                      onClick={() => submitAnswer(quizData.quiz_id, q.id)}
                      disabled={!selectedAnswers[q.id]}
                      className="mt-2 px-3 py-1.5 rounded-md bg-teal text-cream text-sm disabled:opacity-40"
                    >
                      Answer
                    </button>
                  ) : (
                    <p className={`mt-2 text-sm font-medium ${answered[q.id].is_correct ? "text-teal" : "text-brick"}`}>
                      {answered[q.id].is_correct ? "✅ Correct!" : `❌ Incorrect — correct answer: ${answered[q.id].correct_answer}`}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Progress Tab */}
            {activeId === "progress" && (
              <div>
                {progressLoading && (
                  <div className="space-y-3 animate-pulse">
                    {[1, 2, 3].map((i) => (
                      <div key={i} className="h-6 rounded bg-brick/20" />
                    ))}
                  </div>
                )}
                {!progressLoading && progressData?.analysis && (
                  <div className="relative">
                    <div
                      className={`text-sm text-oxblood overflow-hidden transition-[max-height] duration-300 ${
                        progressExpanded ? "max-h-[2000px]" : "max-h-72"
                      }`}
                    >
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          table: ({ node, ...props }) => (
                            <div className="overflow-x-auto rounded-lg border border-oxblood/20 my-3">
                              <table
                                className="w-full text-sm bg-white border-collapse"
                                {...props}
                              />
                            </div>
                          ),
                          thead: ({ node, ...props }) => (
                            <thead className="bg-teal text-cream" {...props} />
                          ),
                          th: ({ node, ...props }) => (
                            <th
                              className="px-3 py-2 text-left font-ui font-medium"
                              {...props}
                            />
                          ),
                          td: ({ node, ...props }) => (
                            <td
                              className="px-3 py-2 border-t border-oxblood/10 bg-white"
                              {...props}
                            />
                          ),
                          tr: ({ node, ...props }) => (
                            <tr className="even:bg-cream/50" {...props} />
                          ),
                        }}
                      >
                        {progressData.analysis}
                      </ReactMarkdown>
                    </div>

                    {/* Fade-out hint over the cut-off content, only when collapsed */}
                    {!progressExpanded && (
                      <div className="pointer-events-none absolute bottom-8 left-0 right-0 h-12 bg-gradient-to-t from-white to-transparent" />
                    )}

                    <button
                      type="button"
                      onClick={() => setProgressExpanded((prev) => !prev)}
                      className="mt-2 text-xs font-ui tracking-wide text-teal underline"
                    >
                      {progressExpanded ? "Show less" : "Show more"}
                    </button>
                  </div>
                )}
              </div>
            )}

      {/* Plan Tab */}
      {activeId === "plan" && (
        <div>
          <input
            value={planQuery}
            onChange={(e) => setPlanQuery(e.target.value)}
            placeholder="Topic to plan..."
            className="w-full px-3 py-2 rounded-md border border-teal text-sm text-oxblood placeholder:text-oxblood/70 focus:outline-none focus:ring-2 focus:ring-teal/40"
          />
          <button
            onClick={submitPlan}
            disabled={planLoading || !planQuery.trim()}
            className="mt-2 px-4 py-2 rounded-md bg-burnt text-teal text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {planLoading ? "Generating..." : "Generate Plan"}
          </button>

          {planLoading && (
            <div className="mt-4 space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-6 rounded bg-brick/20" />
              ))}
            </div>
          )}

          {!planLoading && !planData && (
            <p className="mt-4 text-sm text-oxblood/70">
              Enter a topic above to generate a study plan.
            </p>
          )}

          {!planLoading && planData?.plan && (
            <div className="mt-4 text-sm text-oxblood">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{planData.plan}</ReactMarkdown>
            </div>
          )}
        </div>
      )}

      {/* Research Tab */}
      {activeId === "research" && (
        <div>
          <input
            value={researchQuery}
            onChange={(e) => setResearchQuery(e.target.value)}
            placeholder="Topic to research..."
            className="w-full px-3 py-2 rounded-md border border-teal text-sm text-oxblood placeholder:text-oxblood/70 focus:outline-none focus:ring-2 focus:ring-teal/40"
          />
          <button
            onClick={submitResearch}
            disabled={researchLoading || !researchQuery.trim()}
            className="mt-2 px-4 py-2 rounded-md bg-burnt text-teal text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {researchLoading ? "Generating..." : "Generate Research"}
          </button>

          {researchLoading && (
            <div className="mt-4 space-y-3 animate-pulse">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-6 rounded bg-brick/20" />
              ))}
            </div>
          )}

          {!researchLoading && !researchData && (
            <p className="mt-4 text-sm text-oxblood/70">
              Enter a topic above to research it — using your notes first, the web if needed.
            </p>
          )}

          {!researchLoading && researchData?.answer && (
            <div className="mt-4 text-sm text-oxblood">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{researchData.answer}</ReactMarkdown>
            </div>
          )}
        </div>
      )}
    </div>
  );
}