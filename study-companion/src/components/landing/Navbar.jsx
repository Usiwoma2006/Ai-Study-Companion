import Link from "next/link";

function LandingNav() {
  return (
    <nav className="sticky top-0 z-50 bg-[#335C67] px-6 py-4 flex items-center justify-between">
      <Link href="/" className="font-serif font-bold text-lg text-[#FFF3B0] hover:text-[#FFF3B0]/80 transition-colors">
        🎓 Ethabo
      </Link>

      <div className="flex items-center gap-6">
        <Link 
          href="/login" 
          className="text-[#FFF3B0] underline underline-offset-4 hover:text-[#FFF3B0]/80 transition-colors"
        >
          Login
        </Link>
        
        <Link
          href="/signup"
          className="bg-[#E09F3E] text-[#540B0E] font-semibold px-4 py-2 rounded-lg hover:bg-[#E09F3E]/90 transition-all duration-200 transform hover:scale-105 shadow-md hover:shadow-lg"
        >
          Sign up
        </Link>
      </div>
    </nav>
  );
}

export default LandingNav;