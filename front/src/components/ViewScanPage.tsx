import React, {useEffect, useState} from "react";
import Header from "./Header";
import {useNavigate, useParams} from "react-router-dom";
import toast from "react-hot-toast";
import {Button, Spinner} from "flowbite-react";

const ViewScanPage = () => {
    const {scanId} = useParams<{scanId: string}>()
    const [scanData, setScanData] = useState({'_id': {'$oid': ''}, 'scan_name': '', 'scan_url':'', 'scan_results':{}})
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/scan/${scanId}/get`)
                if (!response.ok) {
                    toast.error("Cannot get the scan with this id")
                }
                const scanData = await response.json()
                setScanData(scanData)
            } catch (error) {
                toast.error("Network error")
            } finally {
                setLoading(false)
            }
        }
        fetchData()
    }, [scanId])

    const formatJSON = (jsonString:string) => {
        const lines = jsonString.split('\n');
        const formattedLines = lines.map((line:string, index:number) => (
            <span key={index} className="block">
        {line.trim() ? (
            <span>
            {line.startsWith(' ') ? (
                <span className="text-gray-400">{line.slice(0, line.length - line.trimStart().length)}</span>
            ) : null}
                <span className="text-gray-800">{line.trimStart()}</span>
          </span>
        ) : (
            <br />
        )}
      </span>
        ));
        return formattedLines;
    };

    const handleDelete = async () => {
        try {
            const response = await fetch(`http://localhost:5000/api/scan/${scanId}/delete`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                toast.error("Network Error")
            } else {
                const jsonData = await response.json()
                navigate(`/scans/list`)
            }


        } catch (error) {
            toast.error("Unable to remove the scan!")
        }
    }

    const handleDownload = async () => {
        try {
            const response = await fetch(`http://localhost:5000/api/scan/${scanId}/download`)
            if (!response.ok) {
                toast.error("Unable to download the report")
            }
            const blob = await response.blob()
            const url = window.URL.createObjectURL(blob)
            window.open(url)
        } catch (error) {
            toast.error("Network Error")
        }
    }

    if (loading) {
        return <div className="w-full h-full flex justify-center"><Spinner className="self-center size-1/6"/></div>
    }

    return (
        <div>
            <Header/>
            {/*<div className="flex">*/}
            {/*    <div className="flex flex-col mr-4">*/}
            {/*        <div className="border border-gray-400 p-2 mb-4">*/}
            {/*            <span className="text-gray-600 font-bold">{scanData['_id']['$oid']}</span>*/}
            {/*        </div>*/}
            {/*        <div className="border border-gray-400 p-2 mb-4">*/}
            {/*            <span className="text-gray-600 italic">{scanData['scan_name']}</span>*/}
            {/*        </div>*/}
            {/*        <div className="border border-gray-400 p-2">*/}
            {/*            <span className="text-gray-600">{scanData['scan_url']}</span>*/}
            {/*        </div>*/}
            {/*        <div className="border border-gray-400 p-2">*/}
            {/*            <a href="#" className="text-gray-600">Delete</a>*/}
            {/*        </div>*/}
            {/*        <div className="border border-gray-400 p-2">*/}
            {/*            <a href="#" className="text-gray-600">Generate a report</a>*/}
            {/*        </div>*/}
            {/*    </div>*/}
            {/*    <div className="border border-gray-400 p-2">*/}
            {/*        <pre*/}
            {/*            className="text-gray-600 font-mono whitespace-pre-wrap">{formatJSON(JSON.stringify(scanData['scan_results'], null, 2))}</pre>*/}
            {/*    </div>*/}
            {/*</div>*/}
            <div className="flex justify-center items-center h-screen">
                <div className="grid grid-rows-10 grid-flow-col gap-y-10 gap-x-10 h-3/4 w-full max-w-5xl p-4">
                    <div className="row-span-10 col-span-8 border-2 border-gray-400 rounded-2xl p-4">
                        <pre
                            className="text-gray-600 font-mono whitespace-pre-wrap w-full h-full overflow-y-auto">{formatJSON(JSON.stringify(scanData['scan_results'], null, 2))}</pre>
                    </div>
                    <div
                        className="row-span-1 col-span-4 border-2 border-gray-400 text-xl font-semibold dark:text-white rounded-2xl p-4 flex justify-center">
                        <span className="self-center">{scanData['_id']['$oid']}</span></div>
                    <div
                        className="row-span-1 col-span-4 border-2 border-gray-400  text-xl font-semibold dark:text-white rounded-2xl p-4 flex justify-center">
                        <span className="self-center">{scanData['scan_name']}</span></div>
                    <div
                        className="row-span-1 col-span-4 border-2 border-gray-400  text-xl font-semibold dark:text-white rounded-2xl p-4 flex justify-center">
                        <span className="self-center">{scanData['scan_url']}</span></div>
                    <div className="row-span-1 col-span-4 rounded-2xl p-4"></div>
                    <div className="row-span-1 col-span-4 p-4"></div>
                    <div className="row-span-1 col-span-4 p-4"></div>
                    <div className="row-span-1 col-span-4 p-4"></div>
                    <div className="row-span-1 col-span-4 p-4"></div>
                    <div className="row-span-1 col-span-4 p-4"></div>
                    <div
                        className="row-span-1 col-span-2 border-2 border-gray-400 rounded-2xl p-4 flex justify-center hover:bg-gray-200 cursor-pointer"
                        onClick={handleDelete}>
                        <span className="self-center">Delete</span></div>
                    <div onClick={handleDownload}
                         className="row-span-1 col-span-2 border-2 border-gray-400 rounded-2xl p-4 flex justify-center hover:bg-gray-200 cursor-pointer">
                        <span className="self-center">Download</span></div>
                </div>
            </div>
        </div>
    )
}

export default ViewScanPage