import { ChartLine, ListCheck, MessageSquare, NotebookPen, Telescope } from "lucide-react";

export const AGENTS = [
    {
        id: 'tutor',
        icon: MessageSquare,
        label: 'Tutor Chat',
        category: 'ASK ANYTHING',
        title: 'Tutor Chat',
        description: 'Ask anything about the notebook and get an answer grounded in the pages you uploaded, with the exact source paragraph quoted back to you. It adapts depth: one line, one page, or one worked example'
    },
    {
        id: 'quiz',
        icon: ListCheck,
        label: 'Quiz Generator',
        category: 'TEST YOURSELF',
        title: 'Quiz Generator',
        description: 'Choose a source, a topic or the whole notebook and get multiple choice, short answer or flashcard sets. Every wrong answer is logged so the questions get harder exactly where you are weakest.'
    },
    {
        id: 'progress',
        icon: ChartLine,
        label: 'Progress Tracker',
        category: 'MY PROGRESS',
        title: 'Progress Tracker',
        description: 'Recall accuracy per topic, time on task and a running list of concepts that keep slipping. No streak confetti — just an honest map of what is solid and what is not.'
    },
    {
        id: 'research',
        icon: Telescope,
        label: 'Research Assistant',
        category: 'GO DEEPER',
        title: 'Research Assistant',  // Fixed typo
        description: 'It reads your notebook, spots the gaps, then pulls definitions, counter-arguments and examples from beyond your uploads — always clearly marked as outside material so you know what came from where'
    },
    {
        id: 'plan',
        icon: NotebookPen,
        label: 'Study Planner',
        category: 'PLAN STUDY',
        title: 'Study Planner',
        description: 'Give it a deadline and the hours you actually have. It splits your sources into spaced sessions, reshuffles when you miss a day, and never plans two heavy topics back to back.'
    }
];