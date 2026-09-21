"use client";

import { useEffect } from "react";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({ children }) {
  useEffect(() => {
    const setGermanDefault = () => {
      const langCookie = "googtrans=/en/de";

      document.cookie = `${langCookie};path=/`;

      if (window.location.hostname !== "localhost") {
        document.cookie = `${langCookie};domain=.${window.location.hostname};path=/`;
      }
    };

    // Only set German once per browser session
    if (!sessionStorage.getItem("german_default_set")) {
      setGermanDefault();
      sessionStorage.setItem("german_default_set", "true");
    }

    window.googleTranslateElementInit = () => {
      new window.google.translate.TranslateElement(
        {
          pageLanguage: "en",
          autoDisplay: false,
        },
        "google_translate_element"
      );
    };

    if (!document.getElementById("google-translate-script")) {
      const script = document.createElement("script");
      script.id = "google-translate-script";
      script.src =
        "//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
      document.body.appendChild(script);
    }

    // Aggressive observer to hide Translate UI elements that pop up during navigation
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1) { // Element node
            const el = node;
            const isTranslateUI =
              el.classList?.contains('skiptranslate') ||
              el.id === 'goog-gt-tt' ||
              el.className?.includes?.('goog-te') ||
              el.className?.includes?.('VIpgJd-ZVi9od');

            if (isTranslateUI) {
              // Don't hide our actual dropdown container
              if (el.id !== 'google_translate_element' && !el.closest('#google_translate_element')) {
                el.setAttribute('style', 'display: none !important; visibility: hidden !important; opacity: 0 !important; pointer-events: none !important;');
              }
            }
          }
        });
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    return () => observer.disconnect();
  }, []);

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >

        <div className="flex justify-end p-1 bg-[#ABB7C4]">
          <div id="google_translate_element"></div>
        </div>

        {children}

        <ToastContainer
          position="top-center"
          autoClose={2000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />


      </body>
    </html>
  );
}

