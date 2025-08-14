package main

import (
	"github.com/gin-gonic/gin"
	"log"
)

type Task struct {
	ID    string `json:"id"`
	Title string `json:"title"`
	Done  bool   `json:"done"`
}

var tasks = []Task{}

// CORS middleware
func CORSMiddleware() gin.HandlerFunc {
	return gin.HandlerFunc(func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Credentials", "true")
		c.Header("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Header("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})
}

func main() {
	r := gin.New()

	r.Use(gin.Logger())
	r.Use(gin.Recovery())
	r.Use(CORSMiddleware())

	r.GET("/health", func(c *gin.Context) {
		c.JSON(200, gin.H{"status": "ok"})
	})

	r.GET("/tasks", func(c *gin.Context) {
		c.JSON(200, tasks)
	})

	r.POST("/tasks", func(c *gin.Context) {
		var task Task
		err := c.BindJSON(&task)
		if err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}
		tasks = append(tasks, task)
		c.JSON(201, task)
	})

	r.PUT("/tasks/:id", func(c *gin.Context) {
		id := c.Param("id")
		for i, task := range tasks {
			if task.ID == id {
				var updatedTask Task
				err := c.BindJSON(&updatedTask)
				if err != nil {
					c.JSON(400, gin.H{"error": err.Error()})
					return
				}
				tasks[i] = updatedTask
				c.JSON(200, updatedTask)
				return
			}
		}
		c.JSON(404, gin.H{"error": "task not found"})
	})

	r.DELETE("/tasks/:id", func(c *gin.Context) {
		id := c.Param("id")
		for i, task := range tasks {
			if task.ID == id {
				tasks = append(tasks[:i], tasks[i+1:]...)
				c.JSON(204, gin.H{})
				return
			}
		}
		c.JSON(404, gin.H{"error": "task not found"})
	})

	log.Fatal(r.Run(":8080"))
}