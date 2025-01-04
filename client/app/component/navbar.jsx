


export default function Navbar(){
    return(
        <div>
            <div  className="bg-black wi-[100%] h-[80px] text-white ">
                <div className="flex items-center h-[100%] justify-between ml-[50px] mr-[50px]">
                    <div>
                        <h2 className="font-semibold text-2xl">Piggy Bank</h2>
                    </div>
                    <div className="flex gap-[100px]"> 
                        <button className=" w-[100px] rounded hover:text-lg hover:text-red-300 hover:duration-200">Dashboard</button>
                        <button className=" w-[100px] rounded hover:text-lg hover:text-red-300 hover:duration-200">Profile</button>
                        <button className=" w-[100px] rounded hover:text-lg hover:text-red-300 hover:duration-200">Logout</button>


                    </div>
                </div>
            </div>
            
        </div>
    )
}