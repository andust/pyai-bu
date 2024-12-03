"use client";

import Image from "next/image";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

// import { Document, Page, pdfjs } from "react-pdf";


const FileViewer = () => {
  const [fileUrl, setFileUrl] = useState<string | null>(null);
  const [fileContentType, setFileContentType] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState<string | null>(null);
  const serarchParams = useSearchParams();
  const fileId = serarchParams.get("id");

  useEffect(() => {
    if (fileId) {
      fetch(
        `${process.env.NEXT_PUBLIC_GENAI_SERIVCE}/api/v1/file/download/${fileId}`,
        {
          credentials: "include",
          method: "GET",
          cache: "no-cache",
        }
      ).then(async (res) => {
        if (res.ok) {
          const contentType =
            res.headers.get("content-type")?.trim().split(";")[0] || "";

          setFileContentType(contentType);

          if (
            contentType.startsWith("image") ||
            contentType === "application/pdf"
          ) {
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            setFileUrl(url);
          } else if (
            contentType === "text/plain" ||
            contentType === "text/csv"
          ) {
            const text = await res.text();
            setFileContent(text);
          } else {
            setFileContent("Unsupported file type");
          }
        }
      });
    }

    return () => {
      if (fileUrl) {
        URL.revokeObjectURL(fileUrl);
      }
    };
  }, [fileId]);

  let fileView = <p>Unsupported or unknown file type</p>;
  const isImage = fileContentType && fileContentType.startsWith("image");
  const isText =
    fileContentType === "text/plain" || fileContentType === "text/csv";
  const isPdf = fileContentType === "application/pdf";
  if (isImage && fileUrl) {
    fileView = (
      <Image
        src={fileUrl}
        alt="Fetched image"
        width="600"
        height="600"
        className="m-auto"
      />
    );
  } else if (isText) {
    fileView = <pre className="whitespace-pre-line">{fileContent}</pre>;
  } else if (isPdf && fileUrl) {
    fileView = (
      <iframe
        src={fileUrl}
        className="w-full aspect-video"
        width="100%"
        height="600px"
        style={{ border: 'none' }}
        title="PDF Viewer"
      />
      // <Document file={fileUrl}>
      //   <Page pageNumber={1} />
      // </Document>
    );
  }

  return fileView;
};

export default FileViewer;
