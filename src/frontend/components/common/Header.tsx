import ThemeToggle from './ThemeToggle';

const Header = () => {
  return (
    <header className="bg-[rgb(var(--bg-primary))] shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <div className="h-8 w-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center">
                <span className="text-white text-sm font-bold">T</span>
              </div>
              <span className="ml-2 text-xl font-bold text-[rgb(var(--text-primary))]">TaskMaster Pro</span>
            </div>
          </div>
          <div className="flex items-center">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;