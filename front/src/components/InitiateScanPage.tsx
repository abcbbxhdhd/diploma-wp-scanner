import React, {useState} from "react";
import Header from "./Header";
import {Button, Label, Spinner, TextInput} from "flowbite-react";
import {useNavigate} from 'react-router-dom'
import toast from "react-hot-toast"

const InitiateScanPage = () => {
    const [name, setName] = useState<string>("")
    const [url, setUrl] = useState<string>("")
    const [loading, setLoading] = useState<boolean>(false)
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setLoading(true)

        try {
            const response = await fetch('http://localhost:5000/api/scan/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'scan_name': name, 'url': url})
            });

            if (!response.ok) {
                toast.error("Network Error")
            } else {
                const jsonData = await response.json()
                navigate(`/scans/view/${jsonData['id']}`)
            }


        } catch (error) {
            toast.error("Unable to execute a scan!")
        }

        setLoading(false)
    }


    return (
        <div>
            <Header/>
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <form className="flex max-w-md flex-col gap-4" onSubmit={handleSubmit}>
                <div>
                    <div className="mb-2 block">
                        <Label htmlFor="scan-name" value="Scan Name"/>
                    </div>
                    <TextInput id="scan-name" name="scan_name" type="text" placeholder="My Scan" required onChange={(event) => setName(event.target.value)}/>
                </div>
                <div>
                    <div className="mb-2 block">
                        <Label htmlFor="scan-url" value="URL"/>
                    </div>
                    <TextInput id="scan-url" name="url" type="text" placeholder="http://localhost:8080" required onChange={(event) => setUrl(event.target.value)}/>
                </div>
                <Button type="submit" disabled={(name==="" || url==="") || loading}>
                    <span>Submit</span> {loading && <Spinner/>}
                </Button>
            </form>
            </div>
            </div>
    )
}

export default InitiateScanPage