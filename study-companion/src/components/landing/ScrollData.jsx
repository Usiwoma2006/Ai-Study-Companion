import { ChartLine, ListCheck, MessageSquare, NotebookPen, Telescope } from "lucide-react";

export const SCROLL_AGENTS = [
    {
        id: 'tutor',
        number: "1",
        icon: MessageSquare,
        title: 'Tutor Chat',
        label: 'A patient tutor that only ever cites your own notes.',
        description: 'Ask anything about the notebook and get an answer grounded in the pages you uploaded, with the exact source paragraph quoted back to you. It adapts depth: one line, one page, or one worked example'
    },
    {
        id: 'quiz',
        number: "2",
        icon: ListCheck,
        title: 'Quiz Generator',
        label: 'Turns any chapter into recall practice in seconds.',
        description: 'Choose a source, a topic or the whole notebook and get multiple choice, short answer or flashcard sets. Every wrong answer is logged so the questions get harder exactly where you are weakest.'
    },
    {
        id: 'progress',
        number: "3",
        icon: ChartLine,
        title: 'Progress Tracker',
        label: 'Shows the weak spots you would rather ignore',
        description: 'Recall accuracy per topic, time on task and a running list of concepts that keep slipping. No streak confetti — just an honest map of what is solid and what is not.'
    },
    {
        id: 'research',
        number: "4",
        icon: Telescope,
        title: 'Research Assistant',
        label: 'Finds what your notes left out', 
        description: 'It reads your notebook, spots the gaps, then pulls definitions, counter-arguments and examples from beyond your uploads — always clearly marked as outside material so you know what came from where'
    },
    {
        id: 'plan',
        number: "5",
        icon: NotebookPen,
        title: 'Study Planner',
        label: 'Works backwards from your exam date',
        description: 'Give it a deadline and the hours you actually have. It splits your sources into spaced sessions, reshuffles when you miss a day, and never plans two heavy topics back to back.'
    }
];