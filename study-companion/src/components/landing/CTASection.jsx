function CTASection() {
  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 sm:gap-6
                    px-6 py-8 sm:py-10 text-center sm:text-left">
      <a
        href="/signup"
        className="bg-oxblood text-cream
                   text-base sm:text-lg md:text-xl
                   font-serif font-semibold
                   px-5 py-3 rounded-lg
                   w-full sm:w-auto text-center
                   hover:bg-opacity-90 transition-all duration-200"
      >
        Start a notebook →
      </a>

      <div className="text-teal text-sm sm:text-base md:text-xl font-serif">
        Free while you are a student — no card
      </div>
    </div>
  );
}

export default CTASection;