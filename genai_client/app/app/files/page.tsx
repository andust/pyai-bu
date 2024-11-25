import Link from "next/link";

import MainLayout from "@/app/_layout/MainLayout";
import { cookies } from "next/headers";
import { getFiles } from "../_utils/fetch/file";
import { DocFile } from "../_models/file";
import FileViewer from "../_molecules/file-viewer/FileViewer";
import { SearchParams } from "../types";

export default async function New({ searchParams }: SearchParams) {
  const { id: selectedId } = await searchParams;
  let files: DocFile[] = [];
  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getFiles(access);
    if (res.ok) {
      files = await res.json();
    }
  } catch (error) {
    console.log(error);
  }
  return (
    <MainLayout>
      <Link href="/files/upload">Upload files</Link>
      <div className="flex py-5 gap-5">
        <div className="flex flex-col space-y-5 w-1/2">
          {files.map(({ id, filename }) => (
            <Link
              key={id}
              href={`/files?id=${id}`}
              className={selectedId === id ? "text-red" : ""}
            >
              {filename}
            </Link>
          ))}
        </div>
        <div className="">
          <FileViewer />
        </div>
      </div>
    </MainLayout>
  );
}
