"use client";
import { useState } from "react";
import Navbar from "../component/navbar";

export default function Login() {
    const [isSignup, setIsSignup] = useState(false);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [errors, setErrors] = useState({});

    const handleLogin = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/auth/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            if (!res.ok) {
                alert("Invalid Credentials!")
                return; 
            }

            const data = await res.json();
            const { access, user } = data;
            localStorage.setItem("access", access);
            localStorage.setItem("username", user.username);
            alert("Login successful!");
            window.location.href = "/profile";
        } catch (err) {
            setErrors({ general: "An unexpected error occurred. Please try again later." });
        }
    };

    const handleSignup = async () => {
        try {
            const res = await fetch("http://127.0.0.1:8000/api/auth/registration", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password1: password,
                    password2: password,
                    email: email
                })
            });

            if (!res.ok) {
                const errorData = await res.json();
                console.log("Error details:", errorData);
                setErrors(errorData); 
                return; 
            }

            alert("Registration is successful!");
            setIsSignup(false);
        } catch (err) {
            console.error("Error during registration:", err);
            alert(err.message);
        }
    };

    return (
        <div className="w-[100vw] h-[100vh] bg-gradient-to-b from-black via-[#2e0304] to-[#530506] overflow-hidden">
            {/* <Navbar /> */}
            <div className="w-full h-full flex justify-center items-center">
                <div className="bg-black w-[500px] h-[500px] py-6 px-8 rounded-lg shadow-lg border border-solid border-white">
                    {!isSignup && (
                        <div className="mb-4">
                            <span className="font-semibold text-white block text-center text-2xl pb-[40px] pt-[20px]">
                                Welcome to PiggyBank!
                            </span>
                        </div>
                    )}
                    <h2 className="text-2xl font-bold text-white text-center mb-6">
                        {isSignup ? "Start your journey today!" : ""}
                    </h2>

                    <form className="flex flex-col gap-4">
                        <div>
                            <label
                                htmlFor="username"
                                className="block text-white mb-2"
                            >
                                Username
                            </label>
                            <input
                                type="text"
                                id="username"
                                placeholder="Enter your username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                required
                            />
                            {errors.username && (
                                <p className="text-red-500 text-sm">{errors.username[0]}</p>
                            )}
                        </div>

                        {isSignup && (
                            <div>
                                <label
                                    htmlFor="email"
                                    className="block text-white mb-2"
                                >
                                    Email
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    placeholder="Enter your email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                    required
                                />
                                {errors.email && (
                                    <p className="text-red-500 text-sm">{errors.email[0]}</p>
                                )}
                            </div>
                        )}

                        <div>
                            <label
                                htmlFor="password"
                                className="block text-white mb-2"
                            >
                                Password
                            </label>
                            <input
                                type="password"
                                id="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                required
                            />
                            {errors.password1 && (
                                <p className="text-red-500 text-sm">{errors.password[0]}</p>
                            )}
                            {errors.general && (
                                <p className="text-red-500 text-sm">{errors.general}</p>
                            )}
                        </div>

                        <button
                            type="button"
                            className="w-full mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 rounded-lg transition-all duration-300"
                            onClick={isSignup ? handleSignup : handleLogin}
                        >
                            {isSignup ? "Sign Up" : "Login"}
                        </button>
                    </form>

                    <p className="text-center text-gray-400 text-sm mt-4">
                        {isSignup
                            ? "Already have an account? "
                            : "Don't have an account? "}
                        <span
                            className="text-red-400 hover:underline cursor-pointer"
                            onClick={() => setIsSignup(!isSignup)}
                        >
                            {isSignup ? "Log in here" : "Sign up here"}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
}
