"use client"

import { useEffect, useState } from "react";
import Navbar from "../component/navbar";

export default function Profile() {
    const [profile, setProfile] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [address, setAddress] = useState("");
    const [bio, setBio] = useState("");

    const fetchProfile = async () => {
        const username = localStorage.getItem("username");
        const access = localStorage.getItem("access");
        if (!username || !access) {
            return;
        }
    
        try {
            const res = await fetch("http://127.0.0.1:8000/get-profile", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${access}`,
                },
            });
    
            const data = await res.json();
    
            if (res.ok) {
                setProfile(data);
                setFirstName(data.first_name);
                setLastName(data.last_name);
                setAddress(data.address);
                setBio(data.bio);
            } else {
                setProfile(null);
            }
        } catch (error) {
            console.error("Error fetching profile:", error);
        }
    };
    
    const handleProfileSubmit = async (e) => {
        e.preventDefault();
    
        const access = localStorage.getItem("access");
        if (!access) {
            alert("User not authenticated.");
            return;
        }
    
        const profileData = {
            first_name: firstName,
            last_name: lastName,
            address: address,
            bio: bio,
        };
    
        try {
            const res = await fetch("http://127.0.0.1:8000/user-profile", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${access}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(profileData),
            });
    
            const data = await res.json();
            console.log(access)
            console.log(data);
            if (!res.ok) {
                throw new Error("Failed to update profile data.");
              } 
            
            alert("Profile updated successfully!");
            fetchProfile();
            setIsEditing(false);
            
        } catch (error) {
            console.error("Error saving profile:", error);
            alert("An error occurred while saving your profile.");
        }
    };
    
    useEffect(() => {
        fetchProfile();
    }, []);
    

    useEffect(() => {
        fetchProfile();
    }, []);

    return (
        <div className="w-[100vw] h-[100vh] bg-gradient-to-b from-black via-[#2e0304] to-[#530506] overflow-hidden">
            <Navbar />
            <div className="w-full h-[500px] flex mt-[100px] justify-center">
                <div className="bg-black w-[500px] py-6 px-8 rounded-lg shadow-lg border border-solid border-white">
                    {!profile ? (
                        <div className="text-center text-white flex flex-col mt-[100px]">
                            <p className="mt-4 mb-4 text-2xl font-bold">Please create your profile to continue.</p>
                            <button
                                className="mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-300"
                                onClick={() => setIsEditing(true)}
                            >
                                Create Profile
                            </button>
                        </div>
                    ) : (
                        <div>
                            <h2 className="text-2xl font-bold text-white text-center"><u>Profile Information</u> </h2>
                            {isEditing ? (
                                <form onSubmit={handleProfileSubmit} className="flex flex-col gap-2">
                                    <div>
                                        <label className="block text-white mb-2">First Name</label>
                                        <input
                                            type="text"
                                            value={firstName}
                                            onChange={(e) => setFirstName(e.target.value)}
                                            className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-white mb-2">Last Name</label>
                                        <input
                                            type="text"
                                            value={lastName}
                                            onChange={(e) => setLastName(e.target.value)}
                                            className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-white mb-2">Address</label>
                                        <input
                                            type="text"
                                            value={address}
                                            onChange={(e) => setAddress(e.target.value)}
                                            className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-white mb-2">Bio</label>
                                        <textarea
                                            value={bio}
                                            onChange={(e) => setBio(e.target.value)}
                                            className="w-full px-4 py-2 text-black rounded-lg focus:outline-none focus:ring focus:ring-red-500"
                                        />
                                    </div>
                                    <button
                                        type="submit"
                                        className="w-full mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 rounded-lg transition-all duration-300"
                                    >
                                        Save Profile
                                    </button>
                                </form>
                            ) : (
                                <div className="text-white text-xl flex flex-col gap-4 mt-10">
                                    <p><strong>First Name:</strong> {profile.first_name}</p>
                                    <p><strong>Last Name:</strong> {profile.last_name}</p>
                                    <p><strong>Email:</strong> {profile.email}</p>
                                    <p><strong>Address:</strong> {profile.address}</p>
                                    <p><strong>Bio:</strong> {profile.bio}</p>
                                    <button
                                        className="mt-4 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-300"
                                        onClick={() => setIsEditing(true)}
                                    >
                                        Edit Profile
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
