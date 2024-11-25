import MainLayout from "@/app/_layout/MainLayout";
import GenerateImageForm from "../_molecules/generate-image-form/GenerateImageForm";

export default async function New() {
  
  return (
    <MainLayout>
      <GenerateImageForm />
    </MainLayout>
  );
}
