const Footer = () => {
  return (
    <footer className="bg-[rgb(var(--bg-secondary))] border-t border-[rgb(var(--border-primary))] py-8 mt-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-4 md:mb-0">
            <div className="h-8 w-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center mr-3">
              <span className="text-white text-sm font-bold">T</span>
            </div>
            <span className="text-xl font-bold text-[rgb(var(--text-primary))]">TaskMaster Pro</span>
          </div>

          <div className="text-center md:text-right">
            <p className="text-[rgb(var(--text-secondary))] text-sm">
              © {new Date().getFullYear()} TaskMaster Pro. All rights reserved.
            </p>
            <p className="text-[rgb(var(--text-secondary))] text-sm mt-1">
              A free and secure task management solution
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-[rgb(var(--border-primary))] text-center">
          <p className="text-[rgb(var(--text-secondary))] text-sm">
            Enjoy Your Work 
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;