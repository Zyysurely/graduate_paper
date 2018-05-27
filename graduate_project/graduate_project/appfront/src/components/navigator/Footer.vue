<template>
  <div>
    <ul class="icons">
				<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
				<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
				<li><a href="#" class="icon fa-google-plus"><span class="label">Google+</span></a></li>
				<li><a href="#" class="icon fa-pinterest"><span class="label">Pinterest</span></a></li>
				<li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
				<li><a href="#" class="icon fa-linkedin"><span class="label">LinkedIn</span></a></li>
		</ul>
  </div>
</template>
<style>
@import url("https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,300italic,400,600");
@import url("font-awesome.min.css");
  .icons {
			padding: 0.75em 2em 0.75em 2em;
			border-radius: 3em;
			border: solid 1px #fff;
			display: inline-block;
			margin: 0 0 3em 0;
	}
  ul.icons {
		cursor: default;
	}
    ul.icons li {
      display: inline-block;
    }

    ul.icons a {
      display: inline-block;
      width: 2.5em;
      height: 2.5em;
      line-height: 2.5em;
      text-align: center;
      border: 0;
    }
	.icon {
		text-decoration: none;
	}
    .icon:before {
      display: inline-block;
      font-family: FontAwesome;
      font-size: 2em;
      text-decoration: none;
      font-style: normal;
      font-weight: normal;
      line-height: 1;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    .icon > .label {
      display: none;
    }
</style>
<script>
  export default {
    name: 'footer'
  }
</script>
