import { cookies } from "next/headers";

import MainLayout from "@/app/_layout/MainLayout";

import { Project } from "../../_models/project";

import { getProject } from "../../_utils/fetch/project";
import { IdParams } from "@/app/types";
import EstimationToolForm from "../../_molecules/estimation-tool-form/EstimationToolForm";
import { Developer } from "@/app/_models/developer";
import { getDevelopers } from "@/app/_utils/fetch/developer";

export default async function ProjectDetail({ params }: IdParams) {
  const projectId = (await params).id || "";
  let project: Project | null = null;
  let developers: Developer[] = [];

  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getProject(access, projectId);
    if (res.ok) {
      project = await res.json();
    }
  } catch (error) {
    console.log(error);
  }

  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getDevelopers(access);
    if (res.ok) {
      developers = await res.json();
    }
  } catch (error) {
    console.log(error);
  }

  return (
    <MainLayout>
      {project && (
        <ul>
          <li>
            <strong>Title:</strong> {project.title}
          </li>
          <li>
            <strong>Description:</strong> {project.description}
          </li>
          <li>
            <strong>Complexity:</strong> {project.complexity}
          </li>
        </ul>
      )}
      <EstimationToolForm projectId={projectId} developers={developers} />
    </MainLayout>
  );
}
