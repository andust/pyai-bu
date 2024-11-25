import MainLayout from "@/app/_layout/MainLayout";
import UploadFilesForm from "@/app/_molecules/upload-files-form/UploadFilesForm";
import Link from "next/link";


export default function New() {
  return (
    <MainLayout>
      <Link href="/files">Back</Link>
      <hr className="my-4" />
      <UploadFilesForm />
    </MainLayout>
  );
}
