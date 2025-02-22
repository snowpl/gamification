// This file is auto-generated by @hey-api/openapi-ts

import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';
import type { CompaniesReadCompanyResponse, ItemsReadItemsData, ItemsReadItemsResponse, ItemsCreateItemData, ItemsCreateItemResponse, ItemsReadItemData, ItemsReadItemResponse, ItemsUpdateItemData, ItemsUpdateItemResponse, ItemsDeleteItemData, ItemsDeleteItemResponse, LoginLoginAccessTokenData, LoginLoginAccessTokenResponse, LoginTestTokenResponse, LoginRecoverPasswordData, LoginRecoverPasswordResponse, LoginResetPasswordData, LoginResetPasswordResponse, LoginRecoverPasswordHtmlContentData, LoginRecoverPasswordHtmlContentResponse, PrivateCreateUserData, PrivateCreateUserResponse, TasksReadTasksData, TasksReadTasksResponse, TasksAssignTaskData, TasksAssignTaskResponse, TasksSubmitTaskData, TasksSubmitTaskResponse, TasksApproveTaskData, TasksApproveTaskResponse, TasksRejectTaskData, TasksRejectTaskResponse, TasksCancelTaskData, TasksCancelTaskResponse, TasksGetEmployeeTasksData, TasksGetEmployeeTasksResponse, TasksGetTasksEventData, TasksGetTasksEventResponse, UsersReadUsersData, UsersReadUsersResponse, UsersCreateUserData, UsersCreateUserResponse, UsersReadUserMeResponse, UsersDeleteUserMeResponse, UsersUpdateUserMeData, UsersUpdateUserMeResponse, UsersUpdatePasswordMeData, UsersUpdatePasswordMeResponse, UsersReadUserMe1Response, UsersRegisterUserData, UsersRegisterUserResponse, UsersReadUserByIdData, UsersReadUserByIdResponse, UsersUpdateUserData, UsersUpdateUserResponse, UsersDeleteUserData, UsersDeleteUserResponse, UtilsTestEmailData, UtilsTestEmailResponse, UtilsHealthCheckResponse } from './types.gen';

export class CompaniesService {
    /**
     * Read Company
     * Retrieve company.
     * @returns CompanyRead Successful Response
     * @throws ApiError
     */
    public static readCompany(): CancelablePromise<CompaniesReadCompanyResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/company/'
        });
    }
    
}

export class ItemsService {
    /**
     * Read Items
     * Retrieve items.
     * @param data The data for the request.
     * @param data.skip
     * @param data.limit
     * @returns ItemsPublic Successful Response
     * @throws ApiError
     */
    public static readItems(data: ItemsReadItemsData = {}): CancelablePromise<ItemsReadItemsResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/items/',
            query: {
                skip: data.skip,
                limit: data.limit
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Create Item
     * Create new item.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns ItemPublic Successful Response
     * @throws ApiError
     */
    public static createItem(data: ItemsCreateItemData): CancelablePromise<ItemsCreateItemResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/items/',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Read Item
     * Get item by ID.
     * @param data The data for the request.
     * @param data.id
     * @returns ItemPublic Successful Response
     * @throws ApiError
     */
    public static readItem(data: ItemsReadItemData): CancelablePromise<ItemsReadItemResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/items/{id}',
            path: {
                id: data.id
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Update Item
     * Update an item.
     * @param data The data for the request.
     * @param data.id
     * @param data.requestBody
     * @returns ItemPublic Successful Response
     * @throws ApiError
     */
    public static updateItem(data: ItemsUpdateItemData): CancelablePromise<ItemsUpdateItemResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/items/{id}',
            path: {
                id: data.id
            },
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Delete Item
     * Delete an item.
     * @param data The data for the request.
     * @param data.id
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static deleteItem(data: ItemsDeleteItemData): CancelablePromise<ItemsDeleteItemResponse> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/items/{id}',
            path: {
                id: data.id
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}

export class LoginService {
    /**
     * Login Access Token
     * OAuth2 compatible token login, get an access token for future requests
     * @param data The data for the request.
     * @param data.formData
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static loginAccessToken(data: LoginLoginAccessTokenData): CancelablePromise<LoginLoginAccessTokenResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/login/access-token',
            formData: data.formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Test Token
     * Test access token
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static testToken(): CancelablePromise<LoginTestTokenResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/login/test-token'
        });
    }
    
    /**
     * Recover Password
     * Password Recovery
     * @param data The data for the request.
     * @param data.email
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static recoverPassword(data: LoginRecoverPasswordData): CancelablePromise<LoginRecoverPasswordResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/password-recovery/{email}',
            path: {
                email: data.email
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Reset Password
     * Reset password
     * @param data The data for the request.
     * @param data.requestBody
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static resetPassword(data: LoginResetPasswordData): CancelablePromise<LoginResetPasswordResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/reset-password/',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Recover Password Html Content
     * HTML Content for Password Recovery
     * @param data The data for the request.
     * @param data.email
     * @returns string Successful Response
     * @throws ApiError
     */
    public static recoverPasswordHtmlContent(data: LoginRecoverPasswordHtmlContentData): CancelablePromise<LoginRecoverPasswordHtmlContentResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/password-recovery-html-content/{email}',
            path: {
                email: data.email
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}

export class PrivateService {
    /**
     * Create User
     * Create a new user.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static createUser(data: PrivateCreateUserData): CancelablePromise<PrivateCreateUserResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/private/users/',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}

export class TasksService {
    /**
     * Read Tasks
     * Retrieve available tasks.
     * @param data The data for the request.
     * @param data.skip
     * @param data.limit
     * @param data.onlyActive
     * @returns AvailableTasksPublic Successful Response
     * @throws ApiError
     */
    public static readTasks(data: TasksReadTasksData = {}): CancelablePromise<TasksReadTasksResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tasks/',
            query: {
                skip: data.skip,
                limit: data.limit,
                only_active: data.onlyActive
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Assign Task
     * Assign task.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns string Successful Response
     * @throws ApiError
     */
    public static assignTask(data: TasksAssignTaskData): CancelablePromise<TasksAssignTaskResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/tasks/assign-task',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Submit Task
     * Submit task.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns TaskEventDomain Successful Response
     * @throws ApiError
     */
    public static submitTask(data: TasksSubmitTaskData): CancelablePromise<TasksSubmitTaskResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/tasks/submit-task',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Approve Task
     * Approve task.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns TaskEventDomain Successful Response
     * @throws ApiError
     */
    public static approveTask(data: TasksApproveTaskData): CancelablePromise<TasksApproveTaskResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/tasks/approve-task',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Reject Task
     * Reject task.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns TaskEventDomain Successful Response
     * @throws ApiError
     */
    public static rejectTask(data: TasksRejectTaskData): CancelablePromise<TasksRejectTaskResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/tasks/reject-task',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Cancel Task
     * Cancel task.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns TaskEventDomain Successful Response
     * @throws ApiError
     */
    public static cancelTask(data: TasksCancelTaskData): CancelablePromise<TasksCancelTaskResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/tasks/cancel-task',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Get Employee Tasks
     * Get employee tasks.
     * @param data The data for the request.
     * @param data.id
     * @returns EmployeeTask Successful Response
     * @throws ApiError
     */
    public static getEmployeeTasks(data: TasksGetEmployeeTasksData): CancelablePromise<TasksGetEmployeeTasksResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tasks/employee-tasks/{id}',
            path: {
                id: data.id
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Get Tasks Event
     * Get events.
     * @param data The data for the request.
     * @param data.id
     * @returns TaskEvent Successful Response
     * @throws ApiError
     */
    public static getTasksEvent(data: TasksGetTasksEventData): CancelablePromise<TasksGetTasksEventResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/tasks/events/{id}',
            path: {
                id: data.id
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}

export class UsersService {
    /**
     * Read Users
     * Retrieve users.
     * @param data The data for the request.
     * @param data.skip
     * @param data.limit
     * @returns UsersPublic Successful Response
     * @throws ApiError
     */
    public static readUsers(data: UsersReadUsersData = {}): CancelablePromise<UsersReadUsersResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/',
            query: {
                skip: data.skip,
                limit: data.limit
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Create User
     * Create new user.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static createUser(data: UsersCreateUserData): CancelablePromise<UsersCreateUserResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Read User Me
     * Get current user.
     * @returns UserWithExperience Successful Response
     * @throws ApiError
     */
    public static readUserMe(): CancelablePromise<UsersReadUserMeResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/me'
        });
    }
    
    /**
     * Delete User Me
     * Delete own user.
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static deleteUserMe(): CancelablePromise<UsersDeleteUserMeResponse> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/users/me'
        });
    }
    
    /**
     * Update User Me
     * Update own user.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static updateUserMe(data: UsersUpdateUserMeData): CancelablePromise<UsersUpdateUserMeResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/me',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Update Password Me
     * Update own password.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static updatePasswordMe(data: UsersUpdatePasswordMeData): CancelablePromise<UsersUpdatePasswordMeResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/me/password',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Read User Me
     * Get current user with skills.
     * @returns UserWithSkills Successful Response
     * @throws ApiError
     */
    public static readUserMe1(): CancelablePromise<UsersReadUserMe1Response> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/me-with-skills'
        });
    }
    
    /**
     * Register User
     * Create new user without the need to be logged in.
     * @param data The data for the request.
     * @param data.requestBody
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static registerUser(data: UsersRegisterUserData): CancelablePromise<UsersRegisterUserResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/users/signup',
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Read User By Id
     * Get a specific user by id.
     * @param data The data for the request.
     * @param data.userId
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static readUserById(data: UsersReadUserByIdData): CancelablePromise<UsersReadUserByIdResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/{user_id}',
            path: {
                user_id: data.userId
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Update User
     * Update a user.
     * @param data The data for the request.
     * @param data.userId
     * @param data.requestBody
     * @returns UserPublic Successful Response
     * @throws ApiError
     */
    public static updateUser(data: UsersUpdateUserData): CancelablePromise<UsersUpdateUserResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/users/{user_id}',
            path: {
                user_id: data.userId
            },
            body: data.requestBody,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Delete User
     * Delete a user.
     * @param data The data for the request.
     * @param data.userId
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static deleteUser(data: UsersDeleteUserData): CancelablePromise<UsersDeleteUserResponse> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/users/{user_id}',
            path: {
                user_id: data.userId
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
}

export class UtilsService {
    /**
     * Test Email
     * Test emails.
     * @param data The data for the request.
     * @param data.emailTo
     * @returns Message Successful Response
     * @throws ApiError
     */
    public static testEmail(data: UtilsTestEmailData): CancelablePromise<UtilsTestEmailResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/utils/test-email/',
            query: {
                email_to: data.emailTo
            },
            errors: {
                422: 'Validation Error'
            }
        });
    }
    
    /**
     * Health Check
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static healthCheck(): CancelablePromise<UtilsHealthCheckResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/utils/health-check/'
        });
    }
    
}