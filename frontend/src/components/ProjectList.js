import {Link} from 'react-router-dom'


const ProjectItem = ({project}) => {
    return (
        <tr>
            <td>
                <Link to={`/project/${project.id}`} >{project.project_users}</Link>
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


const ProjectList = ({projects}) => {
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
            {projects.map((project) => <ProjectItem project={project} />)}
        </table>
    )
}

export default ProjectList