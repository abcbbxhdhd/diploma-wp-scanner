import React, {useEffect, useState} from "react";
import Header from "./Header";
import toast from "react-hot-toast";
import {Table, TableBody, TableCell, TableHead, TableHeadCell, TableRow} from "flowbite-react";

const ViewAllScansPage = () => {
    const [scans, setScans] = useState([])

    useEffect(() => {
        fetch('http://localhost:5000/api/scan/all')
            .then(async response => {
                if (!response.ok) {
                    toast.error("Something wrong happened")
                }
                const jsonData = await response.json()
                setScans(jsonData)
            })
            .catch(error => {
                toast.error("Network Error")
            })
    }, [])

    return (
        <div>
        <Header/>
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
    <div className="overflow-x-auto">
        <Table>
            <TableHead>
                <TableHeadCell>Scan Name</TableHeadCell>
                <TableHeadCell>Scan URL</TableHeadCell>
                <TableHeadCell>
                    <span className="sr-only">View</span>
                </TableHeadCell>
            </TableHead>
            <TableBody className="divide-y">
                {scans.length > 0 && scans.map(s => (
                    <TableRow className="bg-white dark:border-gray-700 dark:bg-gray-800">
                        <TableCell>{s['scan_name']}</TableCell>
                        <TableCell>{s['scan_url']}</TableCell>
                        <TableCell>
                            <a href={`/scans/view/${s['_id']['$oid']}`} className="font-medium text-cyan-600 hover:underline dark:text-cyan-500">
                                View
                            </a>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    </div>
    </div>
        </div>
    )
}

export default ViewAllScansPage