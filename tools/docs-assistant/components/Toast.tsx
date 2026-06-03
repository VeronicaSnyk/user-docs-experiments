import React, { useEffect, useState } from 'react';

interface ToastProps {
  message: string;
}

export const Toast: React.FC<ToastProps> = ({ message }) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (message) {
      setVisible(true);
      const timer = setTimeout(() => {
        setVisible(false);
      }, 2800); // A bit less than the App's timeout to allow for fade out
      return () => clearTimeout(timer);
    }
  }, [message]);

  return (
    <div
      aria-live="assertive"
      className={`fixed bottom-5 right-5 transition-all duration-300 ease-in-out ${
        visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      <div className="bg-sky-500 text-white font-bold py-2 px-4 rounded-lg shadow-lg">
        {message}
      </div>
    </div>
  );
};
