import React from 'react'

class LoginForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            'login': '',
            'password': ''
        }
    }

    handleSubmit(event) {
        this.props.getToken(this.state.login, this.state.password)
        event.preventDefault()
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)} >
                <input type="text" name="login" placeholder="login" onChange={(event) => this.handleChange(event)} value={this.state.login}/>
                <input type="password" name="password" placeholder="password" onChange={(event) => this.handleChange(event)} value={this.state.password} />
                <input type="submit" value="Login" />
            </form>
        )
    }
}

export default LoginForm