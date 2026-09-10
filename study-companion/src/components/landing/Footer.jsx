import Link from "next/link";

function Footer() {
  return (
    <footer className="bg-[#E09F3E] py-12 sm:py-16 px-4 sm:px-6">
      <div className="max-w-6xl mx-auto">
        {/* Main CTA Section */}
        <div className="flex flex-col items-center text-center gap-6 sm:gap-8">
          <h1 className="font-serif text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl
                         text-oxblood leading-tight max-w-4xl">
            Bring one messy folder of notes.
            <span className="block mt-2">Leave with a study plan.</span>
          </h1>

          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 mt-2 sm:mt-4 w-full sm:w-auto">
            <Link
              href="/signup"
              className="px-6 sm:px-8 py-3 sm:py-3.5
                         text-base sm:text-lg md:text-xl font-serif
                         bg-oxblood text-cream rounded-xl
                         hover:bg-opacity-90 transition-all duration-200
                         shadow-md hover:shadow-lg transform hover:-translate-y-0.5
                         text-center"
            >
              Create Your First Notebook
            </Link>

            <Link
              href="/login"
              className="px-6 sm:px-8 py-3 sm:py-3.5
                         text-base sm:text-lg md:text-xl font-serif
                         border-2 border-oxblood text-oxblood rounded-xl
                         hover:bg-oxblood hover:text-cream transition-all duration-200
                         text-center"
            >
              Login
            </Link>
          </div>
        </div>

        {/* Footer bottom with links */}
        <div className="mt-10 sm:mt-16 pt-6 sm:pt-8 border-t border-oxblood/20
                        flex flex-col sm:flex-row justify-between items-center
                        gap-3 sm:gap-4 text-xs sm:text-sm text-oxblood/70 text-center sm:text-left">
          <p>© 2024 Ethabo. All rights reserved.</p>
          <div className="flex gap-4 sm:gap-6">
            <Link href="/privacy" className="hover:text-oxblood transition-colors">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-oxblood transition-colors">
              Terms
            </Link>
            <Link href="/contact" className="hover:text-oxblood transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;