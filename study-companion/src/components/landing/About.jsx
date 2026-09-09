// Add to index.html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400&display=swap" rel="stylesheet" />

function About() {
    return (
        <div className="bg-teal flex flex-col md:flex-row gap-32 px-8 py-16 md:py-20">
            <div className="column text-cream text-3xl font-light leading-relaxed flex items-center">
                <p className="font-['Playfair_Display'] tracking-wide">
                    Ethabo reads only what you give 
                    it. Drop lecture slides, scanned pages 
                    and past papers into a subject notebook, 
                    and five agents get to work on that 
                    material alone.
                </p>
            </div>

            <div className="text-cream text-xl font-light leading-relaxed space-y-6">
                <p>
                    No generic internet answers. Every 
                    explanation, question and plan traces
                    back to a page you uploaded, so revision
                    matches the syllabus you are actually sitting.
                </p>
                <p>
                    One notebook per subject. Sources stay
                    separate, progress stays separate,
                    and the tutor never mixes up your Pharmacology
                    with your Statistics.
                </p>
            </div>

        </div>
    );
}

export default About;