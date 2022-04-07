import {useParams} from 'react-router-dom'


const ProjectItem = ({project}) => {
    return (
        <tr>
            <td>
                {project.project_users}
            </td>
            <td>
                {project.project_name}
            </td>
            <td>
                {project.git_name}
            </td>
        </tr>
    )
}


const ProjectUserList = ({projects}) => {
    var {id} = useParams()
    var filteredProjects = projects.filter((project) => project.project_users.includes(parseInt(id)))

    return (
        <table>
            <th>
                Project_users
            </th>
            <th>
                Project_name
            </th>
            <th>
                Git_name
            </th>
            {filteredProjects.map((project) => <ProjectItem project={project} />)}
        </table>
    )
}

export default ProjectUserList