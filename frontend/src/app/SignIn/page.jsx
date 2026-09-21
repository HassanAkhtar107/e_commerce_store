"use client";
import { loginApi } from "@/Services/authentication";
import Button from "@/UI/Button";
import Link from "next/link";
import React, { useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useRouter } from "next/navigation";

const LoginSchema = Yup.object().shape({
  username: Yup.string()
    .email("Invalid email address")
    .required("Email is required"),
  password: Yup.string()
    .min(4, "Password must be at least 4 characters")
    .required("Password is required"),
});

const SignIn = () => {
  const router = useRouter();

  useEffect(() => {
    const type = localStorage.getItem("type");
    const token = localStorage.getItem("token");

    if (token && type === "ADMIN") {
      router.push("/Dashboard");
    } else if (token && type === "USER") {
      router.push("/User");
    } else {
      router.push("/SignIn");
    }
  }, []);

  const formik = useFormik({
    initialValues: {
      username: "",
      password: "",
    },
    validationSchema: LoginSchema,
    onSubmit: async (values) => {
      const response = await loginApi(values);

      if (response.success) {
        const userType = response.data.user.user_type;

        if (userType === "ADMIN") {
          router.push("/Dashboard");
        } else {
          router.push("/User");
        }
      } else {
        toast.error("Invalid email or password");
      }
    },
  });

  return (
    <div className="w-full h-[calc(100vh-59px)] bg-blue-600 hover:bg-blue-700 grid grid-cols-1 sm:grid-cols-2">
      {/* Left Section */}
      <div className="hidden sm:flex justify-center items-center px-3 py-9 sm:py-20 sm:px-9 relative">
        <div className="w-[50%] h-[50%] absolute left-0 bottom-0">
          <img className="w-full h-full" src="/login.png" />
        </div>
        <div className="w-full h-full bg-gray-400 flex items-center px-3 lg:px-16 rounded-[10px] z-10">
          <p className="text-white text-[18px] sm:text-[30px] text-center">
            Document automation platform for modern organizations
          </p>
        </div>
      </div>

      {/* Right Section */}
      <div className="bg-white sm:rounded-tl-[20px] sm:rounded-bl-[20px] flex justify-center items-center px-3 sm:px-4 lg:px-20">
        <div className="w-full">
          <h1 className="text-[18px] text-[rgb(38,42,65)] font-semibold mt-9">
            Sign in to your account
          </h1>

          {/* Form */}
          <form onSubmit={formik.handleSubmit}>
            {/* Username */}
            <input
              type="email"
              name="username"
              value={formik.values.username}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              placeholder="Email"
              className="w-full border-b py-2 mt-5 focus:outline-none border-gray-400 placeholder-gray-500 dark:text-gray-600"
            />
            {formik.touched.username && formik.errors.username && (
              <div className="text-red-500 text-sm mt-[2px]">
                {formik.errors.username}
              </div>
            )}

            <input
              type="password"
              name="password"
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              placeholder="Password"
              className="w-full border-b py-2 mt-5 focus:outline-none border-gray-400 placeholder-gray-500 dark:text-gray-600"
            />
            {formik.touched.password && formik.errors.password && (
              <div className="text-red-500 text-sm mt-[2px]">
                {formik.errors.password}
              </div>
            )}

            <Link href="forgot-password">
              <h1 className="mt-5 cursor-pointer underline text-gray-700 font-bold text-[14px]">
                Forgot Password?
              </h1>
            </Link>

            <Button type="submit" label="Login" />
          </form>
        </div>
      </div>
    </div>
  );
};

export default SignIn;
