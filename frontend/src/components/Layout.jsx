import BottomNav from "./BottomNav";
export default function Layout({ children, hideNav }) {
  return (
    <div className="min-h-screen bg-[#F5F5F7] flex justify-center">
      <div className="w-full max-w-[480px] bg-[#FDFDFD] min-h-screen relative phone-shell flex flex-col">
        <div className="flex-1 pb-[88px]">
          {children}
        </div>
        {!hideNav && <BottomNav />}
      </div>
    </div>
  );
}
