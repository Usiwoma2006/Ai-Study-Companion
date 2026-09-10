import Link from "next/link";

function LandingNav() {
  return (
    <nav className="sticky top-0 z-50 bg-[#335C67] px-4 sm:px-6 py-3 sm:py-4
                    flex items-center justify-between">
      <Link
        href="/"
        className="font-serif font-bold text-base sm:text-lg text-[#FFF3B0]
                   hover:text-[#FFF3B0]/80 transition-colors whitespace-nowrap"
      >
        🎓 Ethabo
      </Link>

      <div className="flex items-center gap-3 sm:gap-6">
        <Link
          href="/login"
          className="text-sm sm:text-base text-[#FFF3B0] underline underline-offset-4
                     hover:text-[#FFF3B0]/80 transition-colors"
        >
          Login
        </Link>

        <Link
          href="/signup"
          className="bg-[#E09F3E] text-[#540B0E] font-semibold
                     text-sm sm:text-base
                     px-3 py-1.5 sm:px-4 sm:py-2
                     rounded-lg hover:bg-[#E09F3E]/90 transition-all duration-200
                     transform hover:scale-105 shadow-md hover:shadow-lg
                     whitespace-nowrap"
        >
          Sign up
        </Link>
      </div>
    </nav>
  );
}

export default LandingNav;