import MainLayout from "@/app/_layout/MainLayout";
import ProjectCreateEditForm from "../../_molecules/project-create-edit-form/ProjectCreateEditForm";

export default async function New() {
  
  return (
    <MainLayout>
      New project
      <ProjectCreateEditForm />
    </MainLayout>
  );
}
